"""PKL conversion keeps camera identity, calibration and annotations aligned."""
from unittest.mock import patch

import mmengine
import numpy as np
import pytest

from tools.dataset_converters import update_infos_to_v2 as converter
from tools.dataset_converters.nuscenes_camera_order import NUSCENES_CAMERA_NAMES


def raw_sample():
    cameras = {}
    for index, name in reversed(list(enumerate(NUSCENES_CAMERA_NAMES))):
        cameras[name] = dict(
            data_path=f'samples/{name}/{index}.jpg',
            cam_intrinsic=np.diag([100. + index, 200. + index, 1.]),
            sample_data_token=name, timestamp=1000000 + index,
            sensor2ego_rotation=[1., 0., 0., 0.],
            sensor2ego_translation=[float(index), 0., 0.],
            sensor2lidar_rotation=np.eye(3),
            sensor2lidar_translation=np.array([float(index), 0., 0.]))
    return dict(
        token='sample', timestamp=1000000, cams=cameras, sweeps=[],
        ego2global_rotation=[1., 0., 0., 0.],
        ego2global_translation=[0., 0., 0.],
        lidar2ego_rotation=[1., 0., 0., 0.],
        lidar2ego_translation=[0., 0., 0.], lidar_path='unused.bin',
        gt_boxes=np.array([[1., 2., 0., 4., 2., 1.5, 0.]]),
        gt_names=np.array(['car']), gt_velocity=np.array([[2., -1.]]),
        num_lidar_pts=np.array([1]), num_radar_pts=np.array([0]),
        valid_flag=np.array([True]))


def test_v2_conversion_orders_images_and_camera_instances(tmp_path):
    source = tmp_path / 'input.pkl'
    output = tmp_path / 'output'
    output.mkdir()
    sample = raw_sample()
    mmengine.dump(dict(infos=[sample], metadata=dict(version='v1.0-mini')),
                  source)
    with patch.object(converter, 'NuScenes'), patch.object(
            converter, 'get_nuscenes_2d_boxes',
            side_effect=lambda nusc, token, **kwargs: [dict(camera=token)]):
        converter.update_nuscenes_infos(str(source), str(output), 'unused')
    result = mmengine.load(output / 'input.pkl')
    info = result['data_list'][0]
    assert tuple(info['images']) == NUSCENES_CAMERA_NAMES
    assert tuple(info['cam_instances']) == NUSCENES_CAMERA_NAMES
    for index, name in enumerate(NUSCENES_CAMERA_NAMES):
        image = info['images'][name]
        assert image['img_path'] == f'{index}.jpg'
        assert image['sample_data_token'] == name
        assert image['cam2img'][0][0] == 100. + index
        assert image['lidar2cam'][0][3] == -float(index)
        assert info['cam_instances'][name][0]['camera'] == name
    assert result['metainfo']['version'] == 'v1.0-mini'
    assert info['instances'][0]['velocity'] == [2., -1.]
    np.testing.assert_allclose(info['instances'][0]['bbox_3d'],
                               sample['gt_boxes'][0])


def test_v2_conversion_rejects_missing_camera(tmp_path):
    source = tmp_path / 'input.pkl'
    output = tmp_path / 'output'
    output.mkdir()
    sample = raw_sample()
    del sample['cams']['CAM_BACK']
    mmengine.dump(dict(infos=[sample], metadata=dict(version='v1.0-mini')),
                  source)
    with patch.object(converter, 'NuScenes'), pytest.raises(
            ValueError, match='missing NuScenes cameras.*CAM_BACK'):
        converter.update_nuscenes_infos(str(source), str(output), 'unused')
