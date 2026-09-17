# Copyright (c) OpenMMLab. All rights reserved.
"""Validate nuScenes V2 annotations for camera-only FCOS3D and PGD.

This module is both a command-line utility and the post-conversion validator
used by ``tools/create_data.py`` and ``update_infos_to_v2.py``.
"""

import argparse
import json
import math
import os
import pickle
from collections import Counter
from os import path as osp

import numpy as np


CAMERAS = {
    'CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK',
    'CAM_BACK_LEFT', 'CAM_BACK_RIGHT'
}
REQUIRED_INSTANCE_FIELDS = {
    'bbox', 'bbox_3d', 'bbox_label_3d', 'center_2d', 'depth'
}


class ValidationReport:
    """Accumulate validation results and report all failures together."""

    def __init__(self):
        self.failures = []
        self.warnings = []

    def check(self, condition, message):
        if not condition:
            self.failures.append(message)

    def warn(self, condition, message):
        if not condition:
            self.warnings.append(message)

    def finish(self):
        for message in self.warnings:
            print(f'[WARN] {message}')
        if self.failures:
            print('\n=== FCOS3D VALIDATION FAILED ===')
            for message in self.failures:
                print(f'[FAIL] {message}')
            raise RuntimeError(
                f'FCOS3D validation found {len(self.failures)} failure(s).')
        print('\n=== FCOS3D VALIDATION PASSED ===')


def _load_json(metadata_root, name):
    with open(osp.join(metadata_root, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def validate_raw_relationships(metadata_root, report):
    """Validate foreign keys and duplicate annotations in nuScenes JSONs."""
    required = [
        'sensor', 'calibrated_sensor', 'sample', 'sample_data',
        'sample_annotation', 'instance', 'scene', 'ego_pose'
    ]
    missing = [name for name in required
               if not osp.isfile(osp.join(metadata_root, name + '.json'))]
    report.check(not missing,
                 f'raw metadata files missing in {metadata_root}: {missing}')
    if missing:
        return

    tables = {name: _load_json(metadata_root, name) for name in required}
    tokens = {
        name: {row['token'] for row in tables[name]}
        for name in ('sensor', 'calibrated_sensor', 'sample', 'instance',
                     'scene', 'ego_pose')
    }
    checks = {
        'calibrated_sensor -> sensor': sum(
            row['sensor_token'] not in tokens['sensor']
            for row in tables['calibrated_sensor']),
        'sample_data -> calibrated_sensor': sum(
            row['calibrated_sensor_token'] not in tokens['calibrated_sensor']
            for row in tables['sample_data']),
        'sample_data -> sample': sum(
            row['sample_token'] not in tokens['sample']
            for row in tables['sample_data']),
        'sample_data -> ego_pose': sum(
            row['ego_pose_token'] not in tokens['ego_pose']
            for row in tables['sample_data']),
        'sample_annotation -> sample': sum(
            row['sample_token'] not in tokens['sample']
            for row in tables['sample_annotation']),
        'sample_annotation -> instance': sum(
            row['instance_token'] not in tokens['instance']
            for row in tables['sample_annotation']),
        'sample -> scene': sum(
            row['scene_token'] not in tokens['scene']
            for row in tables['sample']),
    }
    print('\n=== RAW JSON RELATIONSHIPS ===')
    for name, count in checks.items():
        print(f'{name:40s}: {count}')
        report.check(count == 0, f'{name} has {count} broken relationship(s)')
    pairs = [(row['sample_token'], row['instance_token'])
             for row in tables['sample_annotation']]
    duplicate_count = sum(
        count - 1 for count in Counter(pairs).values() if count > 1)
    print(f'duplicate sample+instance annotations: {duplicate_count}')
    report.check(duplicate_count == 0,
                 f'raw JSON has {duplicate_count} duplicate annotations')


def _image_exists(data_root, camera, image_path):
    candidates = [
        image_path,
        osp.join(data_root, image_path),
        osp.join(data_root, 'samples', camera, osp.basename(image_path)),
    ]
    return any(osp.isfile(path) for path in candidates)


def _duplicate_instance_count(instances):
    signatures = []
    for obj in instances:
        signature = (
            obj.get('bbox_label_3d'),
            tuple(np.asarray(obj.get('bbox', []), dtype=float).round(6)),
            tuple(np.asarray(obj.get('bbox_3d', []), dtype=float).round(6)),
        )
        signatures.append(signature)
    return sum(count - 1 for count in Counter(signatures).values()
               if count > 1)


def validate_info_file(info_path, data_root, report, expected_samples=None,
                       projection_tolerance=0.1):
    """Validate one train/validation V2 PKL."""
    with open(info_path, 'rb') as f:
        payload = pickle.load(f)
    name = osp.basename(info_path)
    print(f'\n=== {name} ===')
    report.check(isinstance(payload, dict), f'{name} is not a dictionary')
    if not isinstance(payload, dict):
        return set()
    report.check('metainfo' in payload, f'{name} has no metainfo key')
    report.check('data_list' in payload, f'{name} has no data_list key')
    samples = payload.get('data_list', [])
    print(f'samples: {len(samples)}')
    if expected_samples is not None:
        report.check(len(samples) == expected_samples,
                     f'{name} has {len(samples)} samples; expected '
                     f'{expected_samples}')

    counters = Counter()
    label_counts = Counter()
    projection_errors = []
    tokens = set()
    for sample_index, sample in enumerate(samples):
        token = sample.get('token')
        report.check(token is not None,
                     f'{name} sample {sample_index} has no token')
        if token is not None:
            report.check(token not in tokens,
                         f'{name} contains duplicate sample token {token}')
            tokens.add(token)
        images = sample.get('images', {})
        cameras = set(images)
        if cameras != CAMERAS:
            counters['bad_camera_sets'] += 1
        cam_instances = sample.get('cam_instances')
        if not isinstance(cam_instances, dict):
            counters['missing_cam_instances'] += 1
            cam_instances = {}

        for camera in CAMERAS:
            image = images.get(camera)
            if not isinstance(image, dict):
                continue
            image_path = image.get('img_path', '')
            if not image_path or not _image_exists(data_root, camera,
                                                    image_path):
                counters['missing_images'] += 1

            intrinsic = np.asarray(image.get('cam2img', []), dtype=float)
            intrinsic_ok = (intrinsic.shape == (3, 3)
                            and np.isfinite(intrinsic).all()
                            and intrinsic[0, 0] > 0
                            and intrinsic[1, 1] > 0)
            if not intrinsic_ok:
                counters['bad_intrinsics'] += 1

            for matrix_name in ('cam2ego', 'lidar2cam'):
                matrix = np.asarray(image.get(matrix_name, []), dtype=float)
                if matrix.shape != (4, 4) or not np.isfinite(matrix).all():
                    counters['bad_extrinsics'] += 1
                elif matrix_name == 'cam2ego':
                    rotation = matrix[:3, :3]
                    if np.linalg.norm(rotation @ rotation.T - np.eye(3)) > 1e-2:
                        counters['bad_extrinsics'] += 1

            instances = cam_instances.get(camera, [])
            counters['duplicate_cam_instances'] += \
                _duplicate_instance_count(instances)
            for obj in instances:
                counters['instances'] += 1
                if not REQUIRED_INSTANCE_FIELDS.issubset(obj):
                    counters['bad_instances'] += 1
                    continue
                bbox = np.asarray(obj['bbox'], dtype=float)
                box3d = np.asarray(obj['bbox_3d'], dtype=float)
                center = np.asarray(obj['center_2d'], dtype=float)
                try:
                    depth = float(obj['depth'])
                    label = int(obj['bbox_label_3d'])
                except (TypeError, ValueError):
                    counters['bad_instances'] += 1
                    continue
                label_counts[label] += 1
                if (bbox.shape != (4,) or not np.isfinite(bbox).all()
                        or bbox[2] <= bbox[0] or bbox[3] <= bbox[1]):
                    counters['bad_2d_boxes'] += 1
                if (box3d.size < 7 or not np.isfinite(box3d[:7]).all()
                        or np.any(box3d[3:6] <= 0)
                        or np.any(box3d[3:6] > 30)):
                    counters['bad_3d_boxes'] += 1
                    continue
                if not math.isfinite(depth) or depth <= 0:
                    counters['bad_depths'] += 1
                elif abs(depth - float(box3d[2])) > 1e-3:
                    counters['bad_depth_z'] += 1
                yaw = float(box3d[6])
                if yaw < -math.pi - 1e-6 or yaw > math.pi + 1e-6:
                    counters['bad_yaw'] += 1
                velocity = obj.get('velocity')
                if velocity is not None:
                    counters['velocity_records'] += 1
                    if not np.isfinite(np.asarray(velocity, dtype=float)).all():
                        counters['bad_velocity'] += 1
                if (intrinsic_ok and center.size >= 2 and box3d[2] > 0
                        and np.isfinite(center[:2]).all()):
                    uvw = intrinsic @ box3d[:3]
                    if abs(uvw[2]) > 1e-12:
                        projected = uvw[:2] / uvw[2]
                        projection_errors.append(
                            float(np.linalg.norm(projected - center[:2])))

    for key in sorted(counters):
        print(f'{key}: {counters[key]}')
    print(f'label counts: {dict(sorted(label_counts.items()))}')
    structural_failures = [
        'bad_camera_sets', 'missing_cam_instances', 'missing_images',
        'bad_intrinsics', 'bad_extrinsics', 'duplicate_cam_instances',
        'bad_instances', 'bad_2d_boxes', 'bad_3d_boxes', 'bad_depths',
        'bad_depth_z', 'bad_yaw'
    ]
    for key in structural_failures:
        report.check(counters[key] == 0,
                     f'{name}: {key}={counters[key]}')
    report.warn(
        counters['bad_velocity'] == 0,
        f'{name}: bad_velocity={counters["bad_velocity"]}; '
        'NuScenesDataset converts missing velocity to [0, 0] before loss '
        'calculation, but repairing it at the source is preferable.')
    if projection_errors:
        mean_error = float(np.mean(projection_errors))
        max_error = float(np.max(projection_errors))
        over_two = sum(value > 2 for value in projection_errors)
        print(f'projection mean px error: {mean_error:.6f}')
        print(f'projection max px error: {max_error:.6f}')
        print(f'projection errors >2 px: {over_two}')
        report.check(mean_error < projection_tolerance,
                     f'{name}: mean projection error {mean_error:.6f}px is '
                     f'not below {projection_tolerance}px')
    else:
        report.check(False, f'{name}: no centers were available to project')

    categories = payload.get('metainfo', {}).get('categories')
    report.check(isinstance(categories, dict) and categories,
                 f'{name}: metainfo.categories is missing or empty')
    return tokens


def validate_resolved_config(config_path, report):
    """Validate the resolved MMEngine config is camera-only FCOS3D/PGD."""
    from mmengine.config import Config

    cfg = Config.fromfile(config_path)
    model = cfg.get('model', {})
    report.check(model.get('type') == 'FCOSMono3D',
                 f'config model type is {model.get("type")!r}')
    report.check(model.get('bbox_head', {}).get('type') in
                 {'FCOSMono3DHead', 'PGDHead'},
                 'config bbox head is not FCOSMono3DHead or PGDHead')
    for split in ('train_dataloader', 'val_dataloader', 'test_dataloader'):
        dataset = cfg.get(split, {}).get('dataset', {})
        modality = dataset.get('modality', {})
        report.check(modality.get('use_camera') is True,
                     f'{split} does not set use_camera=True')
        report.check(modality.get('use_lidar') is False,
                     f'{split} does not set use_lidar=False')
        pipeline = dataset.get('pipeline', [])
        types = [step.get('type') for step in pipeline if isinstance(step, dict)]
        report.check('LoadImageFromFileMono3D' in types,
                     f'{split} lacks LoadImageFromFileMono3D')
        forbidden = {'LoadPointsFromFile', 'ObjectSample'} & set(types)
        report.check(not forbidden,
                     f'{split} contains point-cloud transforms: {forbidden}')
    print(f'config: {config_path}')


def validate_checkpoint(checkpoint_path, report):
    """Perform a lightweight checkpoint structure check."""
    import torch

    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    state_dict = checkpoint.get('state_dict', checkpoint)
    report.check(isinstance(state_dict, dict) and bool(state_dict),
                 f'{checkpoint_path} has no usable state_dict')
    print(f'checkpoint keys: {len(state_dict)}')


def validate_dataset(data_root, info_paths, metadata_root=None,
                     expected_samples=None, config_path=None,
                     checkpoint_path=None, projection_tolerance=0.1):
    """Run the complete automatable validation suite."""
    report = ValidationReport()
    data_root = osp.abspath(data_root)
    info_paths = [osp.abspath(path) for path in info_paths]
    if metadata_root:
        validate_raw_relationships(osp.abspath(metadata_root), report)
    token_sets = []
    expected_samples = expected_samples or {}
    for info_path in info_paths:
        report.check(osp.isfile(info_path), f'PKL does not exist: {info_path}')
        if not osp.isfile(info_path):
            continue
        split = ('train' if '_train.' in info_path else
                 'val' if '_val.' in info_path else 'test')
        token_sets.append((split, validate_info_file(
            info_path, data_root, report, expected_samples.get(split),
            projection_tolerance)))
    train_tokens = next((tokens for split, tokens in token_sets
                         if split == 'train'), None)
    val_tokens = next((tokens for split, tokens in token_sets
                       if split == 'val'), None)
    if train_tokens is not None and val_tokens is not None:
        overlap = train_tokens & val_tokens
        print(f'\ntrain/val token overlap: {len(overlap)}')
        report.check(not overlap,
                     f'train/val split has {len(overlap)} shared token(s)')
    if config_path:
        validate_resolved_config(config_path, report)
    if checkpoint_path:
        validate_checkpoint(checkpoint_path, report)
    report.warn(False, 'Visual GT alignment still requires manual inspection '
                'of rendered samples.')
    report.warn(False, 'NaN/Inf loss stability must be checked with a short '
                'training run.')
    report.finish()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Validate camera-only FCOS3D NuScenes V2 data.')
    parser.add_argument('--data-root', required=True)
    parser.add_argument('--ann-root', required=True)
    parser.add_argument('--extra-tag', default='nuscenes')
    parser.add_argument('--metadata-root', default=None)
    parser.add_argument('--config', default=None)
    parser.add_argument('--checkpoint', default=None)
    parser.add_argument('--expected-train-samples', type=int, default=None)
    parser.add_argument('--expected-val-samples', type=int, default=None)
    parser.add_argument('--projection-tolerance', type=float, default=0.1)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    paths = [
        osp.join(args.ann_root, f'{args.extra_tag}_infos_train.pkl'),
        osp.join(args.ann_root, f'{args.extra_tag}_infos_val.pkl'),
    ]
    expected = {
        'train': args.expected_train_samples,
        'val': args.expected_val_samples,
    }
    validate_dataset(
        args.data_root,
        paths,
        metadata_root=args.metadata_root,
        expected_samples=expected,
        config_path=args.config,
        checkpoint_path=args.checkpoint,
        projection_tolerance=args.projection_tolerance)
