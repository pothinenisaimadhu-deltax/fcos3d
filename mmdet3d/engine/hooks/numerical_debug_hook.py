"""Fail at the first non-finite PGD training value with batch context."""

from collections.abc import Mapping, Sequence
import math
import numbers

import torch
from mmengine.hooks import Hook
from mmengine.structures import BaseDataElement

from mmdet3d.registry import HOOKS


@HOOKS.register_module()
class NumericalDebugHook(Hook):
    """Check inputs, losses, gradients and parameters during training."""

    priority = 'VERY_HIGH'

    def __init__(self, detect_anomaly=False, check_parameters=True):
        self.detect_anomaly = detect_anomaly
        self.check_parameters = check_parameters
        self._batch_context = 'unknown batch'

    @staticmethod
    def _context(data_batch):
        samples = data_batch.get('data_samples', []) if isinstance(
            data_batch, Mapping) else []
        details = []
        for sample in samples:
            meta = getattr(sample, 'metainfo', {})
            details.append(str({key: meta[key] for key in
                                ('sample_idx', 'token', 'img_path',
                                 'ori_filename') if key in meta}))
        return '; '.join(details) or 'no sample metadata available'

    def _check(self, value, path):
        if isinstance(value, torch.Tensor):
            if (value.is_floating_point() or value.is_complex()) and not \
                    torch.isfinite(value).all():
                bad = (~torch.isfinite(value)).sum().item()
                raise FloatingPointError(
                    f'Non-finite value in {path} ({bad}/{value.numel()}); '
                    f'{self._batch_context}')
        elif isinstance(value, numbers.Real) and not math.isfinite(value):
            raise FloatingPointError(
                f'Non-finite scalar in {path}; {self._batch_context}')
        elif isinstance(value, Mapping):
            for key, child in value.items():
                self._check(child, f'{path}.{key}')
        elif isinstance(value, BaseDataElement):
            for key, child in value.items():
                self._check(child, f'{path}.{key}')
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            for index, child in enumerate(value):
                self._check(child, f'{path}[{index}]')

    def before_train(self, runner):
        if self.detect_anomaly:
            torch.autograd.set_detect_anomaly(True)
        for name, parameter in runner.model.named_parameters():
            if parameter.requires_grad:
                parameter.register_hook(
                    lambda grad, name=name: self._check(grad, f'gradient.{name}')
                    or grad)

    def before_train_iter(self, runner, batch_idx, data_batch=None):
        self._batch_context = (
            f'epoch={runner.epoch + 1}, iter={runner.iter + 1}, '
            f'batch_idx={batch_idx}; {self._context(data_batch)}')
        self._check(data_batch, 'data_batch')
        if self.check_parameters:
            for name, parameter in runner.model.named_parameters():
                self._check(parameter, f'parameter.{name}')

    def after_train_iter(self, runner, batch_idx, data_batch=None, outputs=None):
        self._check(outputs, 'train_outputs')
