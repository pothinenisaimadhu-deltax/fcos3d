# Copyright (c) OpenMMLab. All rights reserved.
"""Prepare NuScenes data for FCOS3D and related NuScenes models."""

import argparse
import os
from os import path as osp

from tools.dataset_converters import nuscenes_converter
from tools.dataset_converters.update_infos_to_v2 import update_pkl_infos


def nuscenes_data_prep(root_path, info_prefix, version, out_dir,
                       max_sweeps=10, nuscenes_path=None,
                       trainval_meta_root=None):
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
        out_dir=out_dir)

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
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    data_root = (args.nuscenes_path
                 if args.nuscenes_path is not None else args.root_path)
    out_dir = osp.abspath(args.out_dir)

    if args.version == 'v1.0-mini':
        nuscenes_data_prep(
            args.root_path, args.extra_tag, args.version, out_dir,
            args.max_sweeps, args.nuscenes_path)
    else:
        nuscenes_data_prep(
            args.root_path, args.extra_tag, f'{args.version}-trainval',
            out_dir, args.max_sweeps, args.nuscenes_path,
            args.trainval_meta_root)
        nuscenes_data_prep(
            args.root_path, args.extra_tag, f'{args.version}-test',
            out_dir, args.max_sweeps, args.nuscenes_path,
            args.trainval_meta_root)
