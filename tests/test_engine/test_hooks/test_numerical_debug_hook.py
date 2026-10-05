# Copyright (c) OpenMMLab. All rights reserved.
"""Tests for the fail-fast PGD numerical diagnostic hook."""

from types import SimpleNamespace
from unittest import TestCase

import torch
from mmengine.config import Config
from torch import nn

from mmdet3d.engine.hooks import NumericalDebugHook


class TestNumericalDebugHook(TestCase):

    def _runner(self, model=None):
        return SimpleNamespace(
            epoch=42, iter=450, model=model or nn.Linear(2, 1))

    def test_finite_batch_and_outputs_pass(self):
        hook = NumericalDebugHook()
        runner = self._runner()
        batch = dict(inputs=torch.ones(1, 2),
                     calibration=[[1.0, 0.0], [0.0, 1.0]])

        hook.before_train_iter(runner, batch_idx=0, data_batch=batch)
        hook.after_train_iter(
            runner, batch_idx=0, data_batch=batch,
            outputs=dict(loss=torch.tensor(0.5)))

    def test_nonfinite_batch_reports_iteration_and_path(self):
        hook = NumericalDebugHook()
        runner = self._runner()
        batch = dict(inputs=torch.tensor([[float('nan'), 1.0]]))

        with self.assertRaisesRegex(
                FloatingPointError,
                r'data_batch\.inputs.*epoch=43, iter=451'):
            hook.before_train_iter(runner, batch_idx=0, data_batch=batch)

    def test_nonfinite_scalar_calibration_is_rejected(self):
        hook = NumericalDebugHook()
        runner = self._runner()
        batch = dict(cam2img=[[1.0, 0.0], [0.0, float('inf')]])

        with self.assertRaisesRegex(FloatingPointError, r'cam2img\[1\]\[1\]'):
            hook.before_train_iter(runner, batch_idx=0, data_batch=batch)

    def test_nonfinite_gradient_is_rejected_during_backward(self):
        model = nn.Linear(1, 1, bias=False)
        hook = NumericalDebugHook()
        hook.before_train(self._runner(model))

        loss = (model(torch.ones(1, 1)) * float('nan')).sum()
        with self.assertRaisesRegex(FloatingPointError, r'gradient\.weight'):
            loss.backward()

    def test_nonfinite_parameter_is_rejected_before_next_batch(self):
        model = nn.Linear(1, 1, bias=False)
        model.weight.data.fill_(float('nan'))
        hook = NumericalDebugHook()

        with self.assertRaisesRegex(FloatingPointError, r'parameter\.weight'):
            hook.before_train_iter(
                self._runner(model), batch_idx=0,
                data_batch=dict(inputs=torch.ones(1, 1)))

    def test_custom_pgd_config_keeps_debugging_and_checkpoints_enabled(self):
        cfg = Config.fromfile('configs/custom/pgd_custom_nuscenes_json.py')

        self.assertTrue(cfg.model.bbox_head.debug_finite)
        self.assertEqual(cfg.log_processor.window_size, 1)
        self.assertTrue(cfg.default_hooks.checkpoint.save_last)
        self.assertEqual(cfg.default_hooks.checkpoint.interval, 1)
        self.assertEqual(
            cfg.default_hooks.checkpoint.save_best,
            'NuScenes metric/pred_instances_3d_NuScenes/NDS')
        self.assertEqual(cfg.val_evaluator.type, 'NuScenesMetric')
        self.assertTrue(cfg.val_evaluator.eval_subset)
