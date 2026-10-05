# Copyright (c) OpenMMLab. All rights reserved.
"""NuScenes camera-only dataset adapter for MV-FCOS3D++.

This adapter is deliberately separate from :class:`NuScenesDataset`: existing
monocular and LiDAR configurations keep their current behaviour.  It makes
the order of the six camera views deterministic and checks that every view
has the calibration matrices used by ``MultiViewDfM``.
"""

from copy import deepcopy
from typing import Union

import numpy as np

from mmdet3d.registry import DATASETS
from .nuscenes_dataset import NuScenesDataset


@DATASETS.register_module()
class NuScenesMultiViewDataset(NuScenesDataset):
    """NuScenesDataset with a deterministic six-camera image layout.

    No point clouds are read.  ``lidar2cam`` is only the name expected by
    MultiViewDfM for a transform from its common 3D reference frame to a
    camera. Boxes must be in the LiDAR reference frame even though point
    clouds are not input. An ego-frame transform is not interchangeable.
    """

    CAMERA_ORDER = (
        'CAM_FRONT_LEFT', 'CAM_FRONT', 'CAM_FRONT_RIGHT',
        'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT')

    # BaseDataset prioritizes class METAINFO over annotation-file metainfo.
    # Do not inherit NuScenesDataset's trainval default: the v2 PKL supplies
    # the real version (mini/trainval), which the evaluator must use.
    METAINFO = {key: value for key, value in NuScenesDataset.METAINFO.items()
                if key != 'version'}

    def parse_data_info(self, info: dict) -> Union[list, dict]:
        # Parent parsers add prefixes in-place. Copy first so repeated dataset
        # access cannot progressively alter paths in the source annotation.
        info = deepcopy(info)
        images = info.get('images')
        if images is None:
            raise KeyError('MV-FCOS3D requires an `images` dictionary.')

        missing_cameras = [name for name in self.CAMERA_ORDER
                           if name not in images]
        if missing_cameras:
            raise KeyError(
                'MV-FCOS3D requires all six NuScenes cameras; missing: '
                f'{missing_cameras}')

        ordered_images = {}
        for camera in self.CAMERA_ORDER:
            camera_info = deepcopy(images[camera])
            if 'img_path' not in camera_info:
                raise KeyError(f'{camera} is missing `img_path`.')
            if 'cam2img' not in camera_info:
                raise KeyError(f'{camera} is missing `cam2img`.')
            if 'lidar2cam' not in camera_info:
                raise KeyError(f'{camera} needs LiDAR-frame `lidar2cam`.')

            camera_info['cam2img'] = np.asarray(
                camera_info['cam2img'], dtype=np.float32)
            camera_info['lidar2cam'] = np.asarray(
                camera_info['lidar2cam'], dtype=np.float32)
            if camera_info['cam2img'].shape not in ((3, 3), (3, 4), (4, 4)):
                raise ValueError(f'{camera}: invalid cam2img shape.')
            if camera_info['lidar2cam'].shape != (4, 4):
                raise ValueError(f'{camera}: lidar2cam must be 4x4.')
            if not (np.isfinite(camera_info['cam2img']).all() and
                    np.isfinite(camera_info['lidar2cam']).all()):
                raise ValueError(f'{camera}: calibration contains NaN/Inf.')
            ordered_images[camera] = camera_info

        info['images'] = ordered_images
        return super().parse_data_info(info)
