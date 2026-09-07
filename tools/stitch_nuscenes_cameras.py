"""Make timestamp-aligned 2x3 NuScenes camera mosaics and an MP4 video.

Example:
    python tools/stitch_nuscenes_cameras.py \
        --input-root data/nuscenes \
        --output-dir work_dirs/camera_mosaic \
        --fps 10

The input is expected to contain samples/<camera_name>/<timestamp>.<ext>.
The six camera folders are aligned by the numeric timestamps in their
filenames.  NuScenes cameras can have slightly different capture times, so
each view is matched to the nearest unused timestamp of the front-camera
anchor frame.
"""

from __future__ import annotations

import argparse
import bisect
from pathlib import Path

import cv2
import numpy as np


CAMERAS = (
    'CAM_FRONT_LEFT',
    'CAM_FRONT',
    'CAM_FRONT_RIGHT',
    'CAM_BACK_LEFT',
    'CAM_BACK',
    'CAM_BACK_RIGHT',
)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', required=True,
                        help='NuScenes root or flat prediction-visuals folder.')
    parser.add_argument('--camera-source-root', default=None,
                        help='NuScenes root used to identify cameras when '
                             '--input-root is a flat folder.')
    parser.add_argument('--output-dir', required=True,
                        help='Directory for stitched PNGs and MP4')
    parser.add_argument('--fps', type=float, default=10.0)
    parser.add_argument('--max-frames', type=int, default=0,
                        help='0 means all complete six-camera frames')
    parser.add_argument('--max-time-delta-us', type=int, default=100000,
                        help='Maximum camera timestamp difference in microseconds.')
    parser.add_argument('--clean-output', action='store_true',
                        help='Remove old generated frames/video in output-dir first.')
    parser.add_argument('--width', type=int, default=640)
    parser.add_argument('--height', type=int, default=360)
    return parser.parse_args()


def indexed_images(input_root: Path, max_time_delta_us: int,
                   camera_source_root: Path | None = None):
    samples_dir = input_root / 'samples'
    if not samples_dir.is_dir():
        files = sorted((
            path for path in input_root.iterdir()
            if path.is_file() and path.suffix.lower() in {'.jpg', '.jpeg', '.png'}),
            key=lambda path: int(path.stem) if path.stem.isdigit() else path.stem)
        if camera_source_root is None:
            return [
                (index, dict(zip(CAMERAS, files[index:index + len(CAMERAS)])),
                 tuple(f'VIEW {i}' for i in range(1, len(CAMERAS) + 1)))
                for index in range(0, len(files) - len(CAMERAS) + 1,
                                   len(CAMERAS))
            ], 0

        # Prediction visualizations are flat, so their filenames do not say
        # which camera produced them.  Recover that information by matching
        # each prediction timestamp to the nearest timestamp in the original
        # NuScenes camera folders.
        reference_root = camera_source_root / 'samples'
        reference = {}
        for camera in CAMERAS:
            camera_dir = reference_root / camera
            if not camera_dir.is_dir():
                raise FileNotFoundError(f'Missing camera directory: {camera_dir}')
            timestamps = sorted(
                int(path.stem) for path in camera_dir.iterdir()
                if path.is_file() and path.stem.isdigit())
            reference[camera] = timestamps
        exact_camera = {}
        duplicate_timestamps = set()
        for camera, timestamps in reference.items():
            for timestamp in timestamps:
                if timestamp in exact_camera:
                    duplicate_timestamps.add(timestamp)
                else:
                    exact_camera[timestamp] = camera

        camera_files = {camera: [] for camera in CAMERAS}
        for path in files:
            if not path.stem.isdigit():
                continue
            timestamp = int(path.stem)
            if timestamp in exact_camera and timestamp not in duplicate_timestamps:
                camera_files[exact_camera[timestamp]].append((timestamp, path))
                continue
            candidates = []
            for camera, timestamps in reference.items():
                position = bisect.bisect_left(timestamps, timestamp)
                for index in (position - 1, position):
                    if 0 <= index < len(timestamps):
                        candidates.append(
                            (abs(timestamps[index] - timestamp), camera))
            if not candidates:
                continue
            delta, camera = min(candidates)
            if delta <= max_time_delta_us:
                camera_files[camera].append((timestamp, path))
        for camera in CAMERAS:
            camera_files[camera].sort(key=lambda item: item[0])
    else:
        camera_files = {}

        for camera in CAMERAS:
            camera_dir = input_root / 'samples' / camera
            if not camera_dir.is_dir():
                raise FileNotFoundError(f'Missing camera directory: {camera_dir}')
            files = [
                path for path in camera_dir.iterdir()
                if path.is_file() and path.suffix.lower() in {'.jpg', '.jpeg', '.png'}
            ]
            if not files or not all(path.stem.isdigit() for path in files):
                raise ValueError(
                    f'Expected numeric timestamp filenames in {camera_dir}.')
            camera_files[camera] = sorted(
                ((int(path.stem), path) for path in files),
                key=lambda item: item[0])

    # CAM_FRONT is the temporal anchor.  Match each other camera to the
    # nearest *unused* timestamp, preserving chronological order.  Pairing by
    # list index is incorrect when one view has a dropped/extra frame.
    anchor = camera_files['CAM_FRONT']
    cursors = {camera: 0 for camera in CAMERAS}
    groups = []
    skipped = 0
    for anchor_timestamp, anchor_path in anchor:
        paths = {'CAM_FRONT': anchor_path}
        proposed_cursors = {}
        valid = True
        for camera in CAMERAS:
            if camera == 'CAM_FRONT':
                continue
            entries = camera_files[camera]
            cursor = cursors[camera]
            if cursor >= len(entries):
                valid = False
                break
            timestamps = [item[0] for item in entries]
            position = bisect.bisect_left(timestamps, anchor_timestamp, cursor)
            candidates = [i for i in (position - 1, position)
                          if cursor <= i < len(entries)]
            selected = min(candidates,
                           key=lambda i: abs(entries[i][0] - anchor_timestamp))
            timestamp, path = entries[selected]
            delta = abs(timestamp - anchor_timestamp)
            if delta > max_time_delta_us:
                valid = False
                break
            paths[camera] = path
            proposed_cursors[camera] = selected + 1
        if valid:
            groups.append((anchor_timestamp, paths, CAMERAS))
            cursors.update(proposed_cursors)
        else:
            skipped += 1
    return groups, skipped


def make_mosaic(paths, width, height, labels):
    tiles = []
    for camera, label in zip(CAMERAS, labels):
        image = cv2.imread(str(paths[camera]))
        if image is None:
            raise RuntimeError(f'Could not read image: {paths[camera]}')
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        cv2.rectangle(image, (0, 0), (width, 32), (0, 0, 0), -1)
        cv2.putText(image, label, (10, 23), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(image)
    return np.vstack((np.hstack(tiles[:3]), np.hstack(tiles[3:])))


def main():
    args = parse_args()
    input_root = Path(args.input_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    frames_dir = output_dir / 'frames'
    frames_dir.mkdir(parents=True, exist_ok=True)

    if args.clean_output:
        for old_frame in frames_dir.glob('*.jpg'):
            old_frame.unlink()
        if (output_dir / 'six_camera_mosaic.mp4').exists():
            (output_dir / 'six_camera_mosaic.mp4').unlink()

    camera_source_root = (Path(args.camera_source_root).resolve()
                          if args.camera_source_root else None)
    groups, skipped = indexed_images(
        input_root, args.max_time_delta_us, camera_source_root)
    complete = groups
    if args.max_frames > 0:
        complete = complete[:args.max_frames]
    if not complete:
        raise RuntimeError('No complete six-camera timestamps were found.')

    frame_paths = []
    video_path = output_dir / 'six_camera_mosaic.mp4'
    video = None
    try:
        for index, (source_index, paths, labels) in enumerate(complete):
            mosaic = make_mosaic(paths, args.width, args.height, labels)
            frame_path = frames_dir / f'{index:06d}_{source_index}.jpg'
            cv2.imwrite(str(frame_path), mosaic)
            frame_paths.append(frame_path)
            if video is None:
                video = cv2.VideoWriter(
                    str(video_path), cv2.VideoWriter_fourcc(*'mp4v'),
                    args.fps, (args.width * 3, args.height * 2))
                if not video.isOpened():
                    raise RuntimeError(f'Could not create video: {video_path}')
            video.write(mosaic)
    finally:
        if video is not None:
            video.release()

    print(f'Created {len(frame_paths)} timestamp-aligned frames: {frames_dir}')
    print(f'Skipped {skipped} anchor frames without six matches within '
          f'{args.max_time_delta_us} us.')
    print(f'Created video: {video_path}')


if __name__ == '__main__':
    main()
