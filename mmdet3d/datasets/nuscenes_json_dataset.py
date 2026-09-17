# Copyright (c) OpenMMLab. All rights reserved.
"""NuScenes-format JSON loader for camera-only FCOS3D and PGD."""

from copy import deepcopy
from os import path as osp
from typing import List

from mmengine import load

from mmdet3d.registry import DATASETS
from .nuscenes_dataset import NuScenesDataset


@DATASETS.register_module()
class NuScenesJsonDataset(NuScenesDataset):
    """Read NuScenes v2 records from JSON without requiring a PKL file."""

    def load_data_list(self) -> List[dict]:
        """Load and validate a NuScenes-format JSON split."""
        if not self.ann_file:
            raise ValueError(
                'NuScenesJsonDataset requires ann_file pointing to a JSON '
                'split manifest.')

        suffix = osp.splitext(self.ann_file)[1].lower()
        if suffix != '.json':
            raise ValueError(
                f'NuScenesJsonDataset expects .json, got {self.ann_file!r}. '
                'Use NuScenesDataset for the original PKL format.')

        payload = load(self.ann_file)
        if isinstance(payload, dict):
            data_list = payload.get('data_list')
            if data_list is None:
                data_list = payload.get('infos')
            if data_list is None:
                raise KeyError(
                    f'{self.ann_file} must contain a data_list array.')
            if payload.get('metainfo'):
                self.metainfo.update(payload['metainfo'])
        elif isinstance(payload, list):
            data_list = payload
        else:
            raise TypeError(
                f'{self.ann_file} must contain a JSON object or list, got '
                f'{type(payload).__name__}.')

        if not data_list:
            raise ValueError(f'{self.ann_file} contains no samples.')

        normalized = []
        for index, raw_record in enumerate(data_list):
            record = deepcopy(raw_record)
            self._validate_record(record, index)
            if not isinstance(record['sample_idx'], int):
                record['sample_idx'] = index
            normalized.append(record)
        return normalized

    def _validate_record(self, record: dict, index: int) -> None:
        """Fail early with a useful message instead of silently empty GT."""
        if not isinstance(record, dict):
            raise TypeError(f'data_list[{index}] must be an object.')
        for field in ('sample_idx', 'token', 'images'):
            if field not in record:
                raise KeyError(f'data_list[{index}] is missing {field!r}.')
        if not isinstance(record['images'], dict) or not record['images']:
            raise ValueError(f'data_list[{index}]["images"] must be non-empty.')

        for camera, image in record['images'].items():
            if not isinstance(image, dict):
                raise TypeError(
                    f'data_list[{index}]["images"][{camera!r}] must be an '
                    'object.')
            for field in ('img_path', 'height', 'width', 'cam2img'):
                if field not in image:
                    raise KeyError(
                        f'data_list[{index}] camera {camera!r} is missing '
                        f'{field!r}.')

        if not self.test_mode:
            if 'ego2global' not in record:
                raise KeyError(f'data_list[{index}] is missing "ego2global".')
            cam_instances = record.get('cam_instances')
            if not isinstance(cam_instances, dict):
                raise KeyError(
                    f'data_list[{index}] needs "cam_instances" for '
                    'camera-only training. Put per-camera 3D boxes there.')
            for camera in record['images']:
                if camera not in cam_instances:
                    raise KeyError(
                        f'data_list[{index}]["cam_instances"] is missing '
                        f'camera {camera!r}.')
