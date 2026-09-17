# Copyright (c) OpenMMLab. All rights reserved.
"""Prepare NuScenes data for FCOS3D and related NuScenes models."""

import argparse
import os
from os import path as osp

from tools.dataset_converters import nuscenes_converter
from tools.dataset_converters.update_infos_to_v2 import update_pkl_infos
from tools.validate_fcos3d_nuscenes import validate_dataset


def nuscenes_data_prep(root_path, info_prefix, version, out_dir,
                       max_sweeps=10, nuscenes_path=None,
                       trainval_meta_root=None, split_json=None,
                       validate=True, expected_samples=None):
    """Create and update NuScenes info files for FCOS3D."""
    data_root = nuscenes_path if nuscenes_path is not None else root_path
    data_root = osp.abspath(data_root)
    out_dir = osp.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    nuscenes_converter.create_nuscenes_infos(
        data_root,
        info_prefix,
        version=version,
        max_sweeps=max_sweeps,
        trainval_meta_root=trainval_meta_root,
        out_dir=out_dir,
        split_json=split_json)

    if version == 'v1.0-test':
        info_paths = [osp.join(out_dir, f'{info_prefix}_infos_test.pkl')]
    else:
        info_paths = [
            osp.join(out_dir, f'{info_prefix}_infos_train.pkl'),
            osp.join(out_dir, f'{info_prefix}_infos_val.pkl'),
        ]

    for info_path in info_paths:
        update_pkl_infos(
            'nuscenes',
            out_dir=out_dir,
            pkl_path=info_path,
            data_root=data_root)

    if validate and version != 'v1.0-test':
        metadata_base = (trainval_meta_root
                         if trainval_meta_root is not None else data_root)
        metadata_root = osp.join(osp.abspath(metadata_base), version)
        project_root = osp.dirname(osp.dirname(osp.abspath(__file__)))
        config_path = osp.join(
            project_root, 'configs', 'fcos3d',
            'fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py')
        validate_dataset(
            data_root,
            info_paths,
            metadata_root=metadata_root,
            expected_samples=expected_samples,
            config_path=config_path)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Prepare NuScenes data for FCOS3D.')
    parser.add_argument('dataset', choices=['nuscenes'])
    parser.add_argument('--root-path', required=True)
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--version', default='v1.0')
    parser.add_argument('--max-sweeps', type=int, default=10)
    parser.add_argument('--extra-tag', default='nuscenes')
    parser.add_argument('--nuscenes-path', default=None,
                        help='Optional sensor/metadata root; defaults to root-path.')
    parser.add_argument('--trainval-meta-root', default=None,
                        help='Optional alternate v1.0-trainval metadata root.')
    parser.add_argument('--split-json', default=None,
                        help='Optional custom train/validation scene split JSON.')
    parser.add_argument(
        '--skip-validation', action='store_true',
        help='Skip the automatic FCOS3D validation after V2 conversion.')
    parser.add_argument('--expected-train-samples', type=int, default=None)
    parser.add_argument('--expected-val-samples', type=int, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    data_root = (args.nuscenes_path
                 if args.nuscenes_path is not None else args.root_path)
    out_dir = osp.abspath(args.out_dir)
    trainval_meta_root = (args.trainval_meta_root
                           if args.trainval_meta_root is not None else data_root)
    split_json = args.split_json
    expected_samples = {
        'train': args.expected_train_samples,
        'val': args.expected_val_samples,
    }
    if split_json is None and args.version != 'v1.0-mini':
        candidate = osp.join(trainval_meta_root,
                             f'{args.version}-trainval', 'splits.json')
        if osp.isfile(candidate):
            split_json = candidate

    if args.version == 'v1.0-mini':
        nuscenes_data_prep(
            args.root_path, args.extra_tag, args.version, out_dir,
            args.max_sweeps, args.nuscenes_path,
            split_json=split_json,
            validate=not args.skip_validation,
            expected_samples=expected_samples)
    else:
        nuscenes_data_prep(
            args.root_path, args.extra_tag, f'{args.version}-trainval',
            out_dir, args.max_sweeps, args.nuscenes_path,
            args.trainval_meta_root, split_json,
            validate=not args.skip_validation,
            expected_samples=expected_samples)
        test_version = f'{args.version}-test'
        test_metadata_dir = osp.join(osp.abspath(data_root), test_version)
        if osp.isdir(test_metadata_dir):
            nuscenes_data_prep(
                args.root_path, args.extra_tag, test_version,
                out_dir, args.max_sweeps, args.nuscenes_path,
                args.trainval_meta_root)
        else:
            print('Skipping {}: metadata directory does not exist: {}'.format(
                test_version, test_metadata_dir))
