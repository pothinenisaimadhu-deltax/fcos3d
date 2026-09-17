"""Validate a custom NuScenes-format JSON manifest before training or test."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--test-mode', action='store_true')
    args = parser.parse_args()
    payload = json.loads(args.manifest.read_text(encoding='utf-8'))
    records = payload.get('data_list', payload.get('infos')) if isinstance(payload, dict) else payload
    if not isinstance(records, list) or not records:
        raise ValueError('manifest must contain a non-empty data_list array')
    for index, record in enumerate(records):
        for key in ('sample_idx', 'token', 'images'):
            if key not in record:
                raise ValueError(f'record {index} is missing {key!r}')
        if not isinstance(record['images'], dict) or not record['images']:
            raise ValueError(f'record {index} has no images')
        for camera, image in record['images'].items():
            missing = {'img_path', 'height', 'width', 'cam2img'} - image.keys()
            if missing:
                raise ValueError(f'record {index}, {camera}: missing {sorted(missing)}')
        if not args.test_mode:
            if 'ego2global' not in record or 'cam_instances' not in record:
                raise ValueError(f'record {index}: training needs ego2global and cam_instances')
            missing = set(record['images']) - set(record['cam_instances'])
            if missing:
                raise ValueError(f'record {index}: cam_instances missing {sorted(missing)}')
    print(f'PASS: {len(records)} records in {args.manifest}')


if __name__ == '__main__':
    main()
