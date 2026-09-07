"""Fine-tune FCOS3D with optional module freezing.

This launcher keeps the source config unchanged and injects fine-tuning
options at runtime.  Typical use on a small target dataset is to freeze the
pretrained backbone for the first few epochs while training the FPN and
FCOS3D head, then unfreeze the backbone for a short lower-learning-rate phase.

Example::

    python tools/finetune_fcos3d.py \
        configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d_finetune.py \
        --work-dir work_dirs/fcos3d_finetune_freeze \
        --freeze backbone --freeze-epochs 2 --backbone-lr-mult 0.1 --amp

``--freeze-epochs 0`` means that the selected modules remain frozen for the
whole run.  Module names may be comma-separated and may refer to nested
modules, for example ``backbone.layer4`` or ``bbox_head``.
"""

import argparse
import logging
import os
import os.path as osp

from mmengine.config import Config, DictAction
from mmengine.hooks import Hook
from mmengine.logging import print_log
from mmengine.registry import HOOKS, RUNNERS
from mmengine.runner import Runner

from mmdet3d.utils import replace_ceph_backend


@HOOKS.register_module()
class FreezeModulesHook(Hook):
    """Freeze selected model modules and optionally unfreeze them by epoch."""

    def __init__(self,
                 module_names,
                 freeze_epochs=0,
                 freeze_batch_norm=True):
        self.module_names = tuple(module_names)
        self.freeze_epochs = int(freeze_epochs)
        self.freeze_batch_norm = bool(freeze_batch_norm)
        self._modules = None

    @staticmethod
    def _unwrap(model):
        return model.module if hasattr(model, 'module') else model

    def _resolve_modules(self, model):
        model = self._unwrap(model)
        resolved = []
        for name in self.module_names:
            current = model
            for part in name.split('.'):
                if not hasattr(current, part):
                    raise AttributeError(
                        f'Cannot freeze "{name}": model has no "{part}" '
                        f'under "{type(current).__name__}"')
                current = getattr(current, part)
            resolved.append((name, current))
        return resolved

    def _set_state(self, frozen):
        for name, module in self._modules:
            module.requires_grad_(not frozen)
            if frozen and self.freeze_batch_norm:
                for child in module.modules():
                    if isinstance(child, torch.nn.modules.batchnorm._BatchNorm):
                        child.eval()
            state = 'frozen' if frozen else 'unfrozen'
            print_log(
                f'Fine-tuning: {state} module {name}',
                logger='current',
                level=logging.INFO)

    def before_train(self, runner):
        self._modules = self._resolve_modules(runner.model)
        # The selected modules start frozen in both modes.  With
        # freeze_epochs == 0 they stay frozen for the complete run.
        self._set_state(True)

    def before_train_epoch(self, runner):
        if self.freeze_epochs > 0:
            should_freeze = runner.epoch < self.freeze_epochs
            self._set_state(should_freeze)


# Imported after the hook declaration so the annotation-free registration
# above remains compatible with the older Python versions used by this repo.
import torch  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(
        description='Fine-tune an FCOS3D model with selective freezing')
    parser.add_argument('config', help='FCOS3D training config')
    parser.add_argument('--work-dir', help='output directory')
    parser.add_argument('--checkpoint', help='pretrained checkpoint override')
    parser.add_argument(
        '--freeze',
        default='backbone',
        help='comma-separated module names to freeze (default: backbone)')
    parser.add_argument(
        '--freeze-epochs',
        type=int,
        default=2,
        help='freeze for this many epochs; 0 freezes for the full run')
    parser.add_argument(
        '--train-frozen-bn',
        action='store_true',
        help='allow BatchNorm statistics to update in frozen modules')
    parser.add_argument(
        '--backbone-lr-mult',
        type=float,
        default=0.1,
        help='LR multiplier for backbone after it is unfrozen')
    parser.add_argument('--batch-size', type=int)
    parser.add_argument('--num-workers', type=int)
    parser.add_argument('--epochs', type=int)
    parser.add_argument('--amp', action='store_true')
    parser.add_argument('--resume', nargs='?', const='auto')
    parser.add_argument('--ceph', action='store_true')
    parser.add_argument(
        '--cfg-options', nargs='+', action=DictAction,
        help='additional config overrides in key=value form')
    parser.add_argument('--launcher', choices=['none', 'pytorch', 'slurm', 'mpi'],
                        default='none')
    parser.add_argument('--local_rank', '--local-rank', type=int, default=0)
    return parser.parse_args()


def _module_names(value):
    names = tuple(part.strip() for part in value.split(',') if part.strip())
    if not names:
        raise ValueError('--freeze must contain at least one module name')
    return names


def main():
    args = parse_args()
    os.environ.setdefault('LOCAL_RANK', str(args.local_rank))

    cfg = Config.fromfile(args.config)
    if args.ceph:
        cfg = replace_ceph_backend(cfg)
    cfg.launcher = args.launcher
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    if args.work_dir:
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir') is None:
        cfg.work_dir = osp.join('./work_dirs', 'fcos3d_finetune_freeze')

    if args.checkpoint:
        cfg.load_from = args.checkpoint
    if args.resume is not None:
        cfg.resume = True
        if args.resume != 'auto':
            cfg.load_from = args.resume

    if args.batch_size is not None:
        cfg.train_dataloader.batch_size = args.batch_size
    if args.num_workers is not None:
        cfg.train_dataloader.num_workers = args.num_workers
    if args.epochs is not None:
        cfg.train_cfg.max_epochs = args.epochs
        for scheduler in cfg.param_scheduler:
            if scheduler.get('by_epoch', False):
                scheduler.end = args.epochs

    if args.amp:
        cfg.optim_wrapper.type = 'AmpOptimWrapper'
        cfg.optim_wrapper.loss_scale = 'dynamic'

    paramwise = cfg.optim_wrapper.setdefault('paramwise_cfg', {})
    custom_keys = paramwise.setdefault('custom_keys', {})
    custom_keys['backbone'] = dict(lr_mult=args.backbone_lr_mult)

    custom_hooks = list(cfg.get('custom_hooks', []))
    custom_hooks.append(
        dict(
            type='FreezeModulesHook',
            module_names=_module_names(args.freeze),
            freeze_epochs=args.freeze_epochs,
            freeze_batch_norm=not args.train_frozen_bn))
    cfg.custom_hooks = custom_hooks

    print_log(f'Fine-tuning config: {args.config}', logger='current')
    print_log(f'Frozen modules: {_module_names(args.freeze)}', logger='current')
    print_log(f'Freeze epochs: {args.freeze_epochs}', logger='current')

    if 'runner_type' not in cfg:
        runner = Runner.from_cfg(cfg)
    else:
        runner = RUNNERS.build(cfg)
    runner.train()


if __name__ == '__main__':
    main()
