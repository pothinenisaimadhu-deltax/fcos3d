"""Regression checks for opt-in NuScenes MV support (no dataset download)."""
from pathlib import Path

import pytest
import torch
from mmengine.config import Config
from mmengine.structures import InstanceData

from mmdet3d.registry import MODELS
from mmdet3d.structures import Det3DDataSample, LiDARInstance3DBoxes
from mmdet3d.utils import register_all_modules


CONFIG = (Path(__file__).resolve().parents[2] / 'configs/mvfcos3d/' /
          'multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py')


def get_config():
    cfg = Config.fromfile(str(CONFIG))
    register_all_modules()
    return cfg


def test_config_and_guards():
    from tools.train import validate_fcos3d_nuscenes_config as train_guard
    from tools.test import validate_fcos3d_nuscenes_config as test_guard
    cfg = get_config()
    train_guard(cfg)
    test_guard(cfg)
    assert cfg.train_dataloader.dataset.with_velocity
    assert not cfg.train_dataloader.dataset.modality.use_lidar
    assert cfg.model.bbox_head_3d.bbox_coder.code_size == 9
    assert round(8 / cfg.model.voxel_size[2]) == 12


def test_velocity_loss_and_prediction():
    cfg = get_config()
    head_cfg = cfg.model.bbox_head_3d.copy()
    head_cfg.train_cfg = cfg.model.train_cfg
    head_cfg.test_cfg = cfg.model.test_cfg.copy()
    head_cfg.test_cfg.score_thr = 0.
    head_cfg.test_cfg.nms_pre = 20
    head = MODELS.build(head_cfg)
    # Assignment, encoding and backwards all work without CUDA.
    priors = head.get_anchors([(2, 2)], [{}], device='cpu')[0][0]
    assert priors.shape[-1] == 9
    target = priors.reshape(-1, 9)[0:1].clone()
    target[:, 7:] = torch.tensor([[2., -1.]])
    sample = Det3DDataSample(metainfo=dict(box_type_3d=LiDARInstance3DBoxes))
    sample.gt_instances_3d = InstanceData(
        bboxes_3d=LiDARInstance3DBoxes(target, box_dim=9),
        labels_3d=torch.zeros(1, dtype=torch.long))
    losses = head.loss([torch.randn(1, 256, 2, 2)], [sample])
    total = sum(sum(values) for values in losses.values())
    assert torch.isfinite(total)
    total.backward()
    grad = head.conv_reg.weight.grad.reshape(head.num_anchors, 9, -1)
    assert grad[:, 7:].abs().sum() > 0
    # CUDA is required by rotated NMS in this MMCV build.
    if torch.cuda.is_available():
        head = head.cuda().eval()
        with torch.no_grad():
            results = head.predict(
                [torch.randn(1, 256, 2, 2, device='cuda')], [sample])
        assert results[0].bboxes_3d.tensor.shape[-1] == 9
        assert len(results[0].bboxes_3d) > 0


def test_dataset_uses_pkl_version_and_camera_order(tmp_path):
    import numpy as np
    from mmengine import dump
    from mmdet3d.registry import DATASETS
    from mmdet3d.datasets.nuscenes_multiview_dataset import NuScenesMultiViewDataset
    cfg = get_config()
    images = {name: dict(img_path='test.jpg', cam2img=np.eye(3),
                         lidar2cam=np.eye(4))
              for name in reversed(NuScenesMultiViewDataset.CAMERA_ORDER)}
    annotation = tmp_path / 'infos.pkl'
    dump(dict(metainfo=dict(version='v1.0-mini'), data_list=[dict(
        sample_idx=0, token='test', images=images, instances=[])]), annotation)
    dataset_cfg = cfg.val_dataloader.dataset.copy()
    dataset_cfg.data_root = str(tmp_path)
    dataset_cfg.ann_file = str(annotation)
    dataset = DATASETS.build(dataset_cfg)
    assert dataset.metainfo['version'] == 'v1.0-mini'
    info = dataset.get_data_info(0)
    assert tuple(info['images']) == NuScenesMultiViewDataset.CAMERA_ORDER


@pytest.mark.skipif(not torch.cuda.is_available(), reason='DCNv2 needs CUDA')
def test_multiview_detector_loss_and_predict():
    cfg = get_config()
    # Keep the actual R101/DCNv2 architecture; reduce only the smoke-test grid.
    cfg.model.backbone.init_cfg = None
    cfg.model.anchor_generator.ranges = [[-2., -2., -5., 2., 2., 3.]]
    cfg.model.bbox_head_3d.anchor_generator.ranges = [
        [-2., -2., 0., 2., 2., 0.]] * 10
    cfg.model.test_cfg.nms_pre = 20
    cfg.model.test_cfg.score_thr = 0.
    model = MODELS.build(cfg.model).cuda()
    camera = torch.eye(4)
    camera[2, 3] = 10.
    intrinsic = torch.tensor([[50., 0., 64.], [0., 50., 64.], [0., 0., 1.]])
    meta = dict(
        box_type_3d=LiDARInstance3DBoxes, num_views=6, num_ref_frames=-1,
        img_shape=[(128, 128)] * 6, input_shape=(128, 128),
        ori_cam2img=[intrinsic.numpy()] * 6,
        lidar2cam=[camera.numpy()] * 6, scale_factor=[(1., 1.)] * 6)
    sample = Det3DDataSample(metainfo=meta)
    sample.gt_instances_3d = InstanceData(
        bboxes_3d=LiDARInstance3DBoxes(
            torch.tensor([[0., 0., 0., 4.08, 1.73, 1.56, 0., 2., -1.]],
                         device='cuda'), box_dim=9),
        labels_3d=torch.zeros(1, dtype=torch.long, device='cuda'))
    inputs = dict(imgs=torch.randn(1, 6, 3, 128, 128, device='cuda'))
    model.train()
    losses = model.loss(inputs, [sample])
    total = sum(sum(values) for values in losses.values())
    assert torch.isfinite(total)
    total.backward()
    model.eval()
    with torch.no_grad():
        outputs = model.predict(inputs, [sample])
    assert outputs[0].pred_instances_3d.bboxes_3d.tensor.shape[-1] == 9
    assert 'pred_instances' in outputs[0]
