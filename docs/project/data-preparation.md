# Data preparation and geometry contract

## Expected dataset layout

```text
data/
  nuscenes/
    samples/
      CAM_FRONT_LEFT/
      CAM_FRONT/
      CAM_FRONT_RIGHT/
      CAM_BACK_LEFT/
      CAM_BACK/
      CAM_BACK_RIGHT/
      LIDAR_TOP/              # standard converter may inspect availability
    sweeps/                   # required by recipes that generate sweep metadata
    maps/
    v1.0-mini/                # or v1.0-trainval; JSON metadata tables
  nuscenes_infos/
    nuscenes_infos_train.pkl
    nuscenes_infos_val.pkl
```

The root passed to conversion contains the version folder, not the JSON
folder itself. Mini uses `v1.0-mini`, not `v1.0-trainval`. Do not rename a
metadata folder to pretend it is a different split/version.

Standard NuScenes metadata includes samples, sample data, annotations, ego
poses, calibrated sensors, sensors, scenes, logs, categories and instances.
Images, calibration and GT must all refer to the same recording/sample.
Dataset files are not distributed with this code.

## Canonical camera order

```python
camera_names = [
    'CAM_FRONT_LEFT', 'CAM_FRONT', 'CAM_FRONT_RIGHT',
    'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT'
]
```

`tools/dataset_converters/nuscenes_camera_order.py` defines this order.
Raw conversion and the v2 updater use it. V2 `images` and `cam_instances`
are keyed by the camera name and written in this order; the MV adapter
enforces the same ordering when loading. Calibration and image identity are
reordered together. Missing required cameras fail explicitly.

A six-camera sample is one MV model sample, not six independent samples.
Mono `load_type='mv_image_based'` expands camera views into separate image
samples; despite the name, it does not fuse six cameras in the network.

## Generate new v2 PKLs

From the repository root:

```bash
python -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/nuscenes_infos --extra-tag nuscenes --version v1.0-mini
```

For trainval:

```bash
python -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/nuscenes_infos --extra-tag nuscenes --version v1.0
```

The trainval command resolves the trainval version and only processes test
metadata if it exists. The Mini command must explicitly use `v1.0-mini`.
The entrypoint generates legacy infos, converts them to v2 in the output
directory, and invokes the mono dataset validator unless skipped.

Choose a **new output directory** for regeneration. The same prefix/directory
can overwrite previously generated PKLs. Keep raw data and existing experiment
PKLs immutable. This code update does not retroactively rewrite old files.

Optional arguments include `--max-sweeps`, `--split-json`,
`--trainval-meta-root`, expected sample counts and `--skip-validation`.
Skipping validation is not evidence of correctness. The automatic validator
checks mono-specific fields; do not pass an MV config to its mono config check.

## PKL structure

```text
metainfo
  categories                 name-to-label mapping
  version                    v1.0-mini or v1.0-trainval
  dataset / info_version
data_list[]                  one frame-level record
  sample_idx / token / timestamp
  ego2global
  lidar_points.lidar2ego      coordinate metadata, not loaded point input
  images[CAM_*]
    img_path
    cam2img
    cam2ego
    lidar2cam
    sample_data_token / timestamp
  instances[]                frame-level common-coordinate GT
    bbox_3d / bbox_label_3d
    velocity / validity / point-count metadata
  cam_instances[CAM_*][]      per-view monocular annotations
    camera-frame bbox_3d
    bbox / center_2d / depth / attributes / velocity as generated
```

For basename image paths, config prefixes point to `samples/<camera>`.
Absolute paths can remain machine-specific; avoid them in portable/public
artifacts. A prefix plus an already-prefixed relative path can duplicate
directories. Do not repair paths by changing geometry.

## Coordinates, calibration and time

Mono uses camera-coordinate GT through per-view annotations. MV uses
LiDAR-coordinate frame-level GT and projects a shared grid into each camera.
No LiDAR point loader is used by the MV recipe.

For column-vector transforms at the same ego pose:

```python
lidar2cam = np.linalg.inv(cam2ego) @ lidar2ego
```

If camera and LiDAR captures have different ego poses, include those pose
transforms; the same-pose shortcut is insufficient. The converter accounts
for sensor/ego/global transforms when constructing sensor-to-LiDAR relations.
Check the actual converter conventions rather than transposing blindly.

Never rename `ego2cam` to `lidar2cam` while retaining LiDAR-frame GT.
Transform boxes, yaw, velocity and evaluation metadata consistently if the
common frame changes. NuScenes boxes and this framework can use different
dimension/center conventions; use tested conversion functions, not a guessed
length/width swap or fixed yaw offset.

Mini metadata version is taken from the PKL by the MV adapter. In mono,
NuScenesDataset's inherited trainval version may need an explicit
`metainfo.version='v1.0-mini'` override in dataloaders.

## Resize and augmentation

The MV baseline preserves original intrinsics as `ori_cam2img` and applies
per-view resize scale factors during feature projection. Using original
intrinsics without the scale factor is wrong; applying both a resized matrix
and the same scale again is also wrong.

The baseline disables crop/flip until geometry is verified. If enabled,
projection metadata such as crop offsets, flips and image shape must be
packed consistently for every camera. A flip of image content alone is not
necessarily invalid when projection explicitly handles it; trace the full
sampling path before changing GT.

## Validation before training

```bash
python tools/validate_fcos3d_nuscenes.py --data-root data/nuscenes --ann-root data/nuscenes_infos --metadata-root data/nuscenes/v1.0-mini
```

Inspect ten diverse samples by rendering complete GT box corners, not only
centers. Check identity, yaw, dimensions, positive depth and projection after
resize. Check all six cameras for MV. Review velocity distributions by class
and finite/nonfinite counts: a zero target can represent a stationary object
and is not by itself a broken annotation.

Untrusted PKLs can execute code during deserialization. Load only data from
trusted sources. Keep customer imagery, tokens and recordings out of public
releases unless release rights and privacy review have been completed.

For custom JSON mono data, start from
[`fcos3d_custom_nuscenes_data_requirements.md`](../fcos3d_custom_nuscenes_data_requirements.md)
and `tools/validate_custom_nuscenes_json.py`. Its evaluator/export contract
differs from official NuScenesMetric.
