"""One-batch camera-only MV training, prediction and evaluator smoke test.

This does not update a checkpoint or measure useful detection accuracy.
Use --small for a low-memory test of the same code path, without downloads.
"""
import argparse
import logging
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
from mmengine.config import Config
from mmengine.dataset import pseudo_collate
from mmengine import dump, load
from mmengine.logging import MMLogger

from mmdet3d.registry import DATASETS, METRICS, MODELS
from mmdet3d.utils import register_all_modules


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', required=True)
    parser.add_argument('--train-ann', required=True)
    parser.add_argument('--val-ann', required=True)
    parser.add_argument('--small', action='store_true')
    args = parser.parse_args()
    config = Path(__file__).resolve().parents[1] / (
        'configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py')
    cfg = Config.fromfile(str(config))
    register_all_modules()
    if not torch.cuda.is_available():
        raise RuntimeError('This R101/DCNv2 smoke test requires CUDA.')
    for split, ann in [('train', args.train_ann), ('val', args.val_ann)]:
        dataset_cfg = cfg[f'{split}_dataloader'].dataset
        dataset_cfg.data_root = args.data_root
        dataset_cfg.ann_file = ann
        dataset_cfg.indices = 1
        if args.small:
            for step in dataset_cfg.pipeline:
                if step.type == 'MultiViewWrapper':
                    step.transforms[0].scale = (320, 180)
    if args.small:
        cfg.model.anchor_generator.ranges = [[-10., -10., -5., 10., 10., 3.]]
        cfg.model.bbox_head_3d.anchor_generator.ranges = [
            [-10., -10., 0., 10., 10., 0.]] * 10
        cfg.model.test_cfg.nms_pre = 100
    # Exercise the computation independently of network/checkpoint downloads.
    cfg.model.backbone.init_cfg = None
    train = DATASETS.build(cfg.train_dataloader.dataset)
    val = DATASETS.build(cfg.val_dataloader.dataset)
    model = MODELS.build(cfg.model).cuda()
    logger = MMLogger.get_current_instance()
    previous_level = logger.level
    logger.setLevel(logging.WARNING)
    try:
        model.init_weights()
    finally:
        logger.setLevel(previous_level)
    model.train()
    batch = model.data_preprocessor(pseudo_collate([train[0]]), training=True)
    print('Training images:', tuple(batch['inputs']['imgs'].shape), flush=True)
    print('GT boxes:', tuple(batch['data_samples'][0].gt_instances_3d.
                             bboxes_3d.tensor.shape), flush=True)
    losses = model.loss(batch['inputs'], batch['data_samples'])
    total = sum(sum(v) if isinstance(v, list) else v for v in losses.values())
    if not torch.isfinite(total):
        raise RuntimeError(f'Nonfinite loss: {losses}')
    total.backward()
    print('Finite training loss and backward:', float(total.detach()), flush=True)
    model.zero_grad(set_to_none=True)
    model.eval()
    with torch.no_grad():
        predictions = model.val_step(pseudo_collate([val[0]]))
    boxes = predictions[0].pred_instances_3d.bboxes_3d.tensor
    assert boxes.shape[-1] == 9
    assert torch.isfinite(boxes).all()
    print('9D predictions:', tuple(boxes.shape), flush=True)
    evaluator_cfg = cfg.val_evaluator.copy()
    evaluator_cfg.data_root = args.data_root
    evaluator_cfg.eval_subset = True
    # The subset evaluator requires exactly the info-file tokens, not a partial
    # prediction file against the full validation PKL. Keep source PKLs intact.
    with tempfile.TemporaryDirectory() as directory:
        subset = load(args.val_ann)
        subset['data_list'] = subset['data_list'][:1]
        evaluator_cfg.ann_file = str(Path(directory) / 'subset.pkl')
        dump(subset, evaluator_cfg.ann_file)
        metric = METRICS.build(evaluator_cfg)
        metric.dataset_meta = val.metainfo
        metric.process({}, [sample.to_dict() for sample in predictions])
        scores = metric.evaluate(1)
    print('Evaluator completed:', {
        key: value for key, value in scores.items()
        if key.endswith('/mAP') or key.endswith('/NDS')}, flush=True)
    print('SMOKE PASSED (not a trained-model accuracy result).')


if __name__ == '__main__':
    main()
