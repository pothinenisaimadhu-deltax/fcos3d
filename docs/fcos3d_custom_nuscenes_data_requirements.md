# Custom data requirements for camera-only FCOS3D

This document defines the data contract for the camera-only FCOS3D project in
this repository and identifies what must be available before Karfic data can
be converted and trained.

## Scope

The active configuration is `FCOSMono3D` with `NuScenesDataset`:

- `use_camera=True`
- `use_lidar=False`
- `load_type='mv_image_based'`
- `box_type_3d='Camera'`
- six camera names: `CAM_FRONT`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`,
  `CAM_BACK`, `CAM_BACK_LEFT`, and `CAM_BACK_RIGHT`
- `pred_attrs=True` and `pred_velo=True`

The network receives image tensors. Calibration, poses, timestamps, and
labels are metadata/targets used by the loader, loss, decoding, and
evaluation; they are not extra image channels.

## Required-data checklist

| Item | Camera-only FCOS3D | FCOS3D++ / multi-camera extension |
|---|---|---|
| RGB images | Required for every training sample and camera view | Required for every synchronized view |
| Image dimensions | Required and must match the calibration frame | Required per camera |
| Camera intrinsics | Required: focal lengths and principal point | Required for every camera |
| Camera-to-ego extrinsics | Required by the NuScenes-style converter | Required for cross-camera geometry |
| Ego/global pose | Required by the current NuScenes conversion path; needed for global-to-camera conversion and velocity | Required when views/frames are aligned through a common ego frame |
| 3D boxes | Required for supervised training | Required for each visible object/view or a common-frame annotation |
| Class labels | Required; must map to configured classes | Required and consistent across views |
| Dimensions | Required: width, length, height | Required |
| 3D center/location | Required in a documented coordinate frame | Required in a common frame or transformable to each camera |
| Yaw/orientation | Required with a documented axis/sign convention | Required |
| 2D center and depth | Required by the current FCOS3D target pipeline, or derived exactly | Required per camera view |
| Velocity | Required by the current head (`pred_velo=True`), or disable that head | Optional for static detection, required if velocity is trained |
| Sample/frame ID | Required and unique | Required and shared across synchronized views |
| Timestamp | Required for temporal ordering; strongly required for multi-camera matching | Required for synchronization |
| Train/validation split | Required; split by scene/sequence where possible | Required and leakage-safe |

## Dataset field specification

The preferred converted format is a v2-style PKL with a top-level structure:

```python
{
    'metainfo': {
        'dataset': 'nuscenes',
        'version': 'custom-karfic',
        'classes': [...],
        'info_version': '1.1',
    },
    'data_list': [sample_record, ...],
}
```

Each `sample_record` should contain:

```python
{
    'sample_idx': 'unique_frame_id',
    'token': 'unique_sample_token',
    'timestamp': 1710000000.123456,
    'ego2global': [[...], [...], [...], [...]],
    'images': {
        'CAM_FRONT': {
            'img_path': 'samples/CAM_FRONT/frame.jpg',
            'height': 900,
            'width': 1600,
            'cam2img': [[fx, 0, cx], [0, fy, cy], [0, 0, 1]],
            'cam2ego': [[...], [...], [...], [...]],
            'timestamp': 1710000000.123456,
            'sample_data_token': 'unique_camera_frame_id',
        },
    },
    'instances': [
        {
            'bbox_3d': [x, y, z, width, length, height, yaw, vx, vy],
            'bbox_label_3d': 0,
            'bbox_3d_isvalid': True,
            'bbox': [x1, y1, x2, y2],
            'center_2d': [u, v],
            'depth': z_camera,
            'velocity': [vx_camera, vy_camera],
            'attr_label': 0,
        },
    ],
}
```

Names can differ in an adapter, but the semantics must not. The current
converter starts from legacy NuScenes-style fields and produces the v2 fields
`images`, `instances`, `bbox_3d`, `bbox_label_3d`, `center_2d`, `depth`, and
`velocity`.

### Images

- Use readable RGB/BGR image files supported by the image loader, normally
  JPEG or PNG.
- Keep the original image dimensions in metadata.
- Store paths relative to the dataset root, not absolute workstation paths.
- Every referenced path must exist and load without corruption.
- Do not resize files offline unless the camera intrinsics are resized by the
  same affine transform.

### Calibration and poses

`cam2img` is the camera intrinsic projection matrix. At minimum it must
contain `fx`, `fy`, `cx`, and `cy` in the same pixel coordinate frame as the
image.

`cam2ego` is a 4x4 camera-to-vehicle transform. `ego2global` is a 4x4 pose
for the vehicle at the sample timestamp. Quaternions may be retained in a
legacy source format, but the converter must produce unambiguous matrices or
validated quaternion order.

If boxes are stored globally, the conversion must apply:

```text
global -> ego -> camera
```

with the correct translation, rotation, axis convention, and timestamp. A
plausible-looking image is not sufficient evidence that these transforms are
correct.

### 3D annotations

For every trainable object, provide:

- class name and mapped integer class ID;
- center/location `(x, y, z)`;
- dimensions `(width, length, height)` in metres;
- yaw/orientation in radians;
- coordinate frame and origin definition;
- visibility/validity flag if objects can be truncated or occluded.

For this configuration, the box is represented in camera coordinates. The
box origin and yaw sign must match `CameraInstance3DBoxes`; do not copy a
LiDAR-frame box directly into a camera-frame field.

`center_2d=[u,v]` is the projected 3D center, not necessarily the rectangle
center. `depth` is the positive camera-axis depth of that 3D center. These
must be derived with the same `cam2img` used by the image.

### Velocity and attributes

The current FCOS3D head predicts velocity and attributes. The converter’s
NuScenes path produces camera-frame velocity from global velocity and poses.
Karfic needs either:

1. valid object velocity vectors and an agreed frame/unit convention; or
2. a deliberate configuration change to disable velocity prediction.

Do not silently substitute zero velocity for moving objects. Attributes are
also optional in many custom datasets; either provide a documented mapping or
disable attribute prediction and remove its target loading requirement.

## nuScenes versus Karfic

| Requirement | nuScenes reference | Karfic status in this checkout |
|---|---|---|
| Image files | Six named camera folders with sample-data records | Not verified; Karfic raw images are not present in the repository |
| Unique sample token | `sample.token` | Not verified |
| Per-camera frame token | `sample_data.token` | Not verified |
| Timestamps | Microsecond timestamps on samples/sample_data | Not verified |
| Camera intrinsics | `calibrated_sensor.camera_intrinsic` | Not verified |
| Camera-to-ego pose | `calibrated_sensor.translation/rotation` | Not verified |
| Ego-to-global pose | `ego_pose.translation/rotation` | Not verified |
| 3D boxes | `sample_annotation` center, size, rotation | Not verified |
| Class taxonomy | NuScenes categories mapped to 10 configured classes | Not verified; class mapping is required |
| Velocity | Derived from NuScenes box velocity and poses | Not verified |
| 2D center/depth | Derived by projecting the camera-frame 3D center | Not verified |
| Converted PKL | Legacy `infos` converted to v2 `data_list` | No Karfic PKL is available locally for inspection |
| Multi-camera synchronization | Shared sample plus per-camera timestamps | Not verified |

This is an evidence boundary, not a claim that Karfic lacks the fields. The
current checkout contains the converter and ignored local NuScenes/data paths,
but no accessible Karfic manifest, annotation sample, calibration export, or
Karfic PKL to inspect.

## Likely gaps to resolve for Karfic

Before training, obtain and validate:

1. A complete image manifest with camera name, relative path, image size,
   frame ID, and timestamp.
2. Intrinsics for every camera and the exact image resolution at calibration
   time.
3. Camera-to-ego extrinsics, with transform direction explicitly documented.
4. Ego pose per frame if annotations are global or if velocity is retained.
5. 3D object annotations with dimensions, center, yaw, class, and coordinate
   frame.
6. A class mapping to the ten configured NuScenes-style classes, or a reduced
   class list and matching model configuration.
7. Projected `center_2d` and positive camera depth, preferably generated by the
   converter rather than hand-entered.
8. Velocity vectors or a decision to disable velocity prediction.
9. Stable unique tokens and scene/frame IDs, with no duplicate top-level
   tokens.
10. A synchronization policy and maximum timestamp difference for FCOS3D++.

## Recommendations

- Keep Karfic source images, annotations, and calibration in their existing
  storage. Generate only manifests/PKLs in the project output directory.
- Write a Karfic-to-NuScenes adapter that emits the v2 `data_list` contract;
  do not fake missing global poses or tokens.
- Validate every metadata table read-only before conversion: every record must
  be an object with a unique non-empty string `token`.
- Validate image existence, image dimensions, finite calibration values,
  positive projected depths, and class IDs before training.
- Use `Resize3D` for train and test pipelines so `centers_2d` and `cam2img`
  follow image resizing.
- For multi-camera training, group views by a shared frame ID and timestamp;
  do not pair independently sorted camera filenames.
- Start with `format_only=True` for custom tokens. Official NuScenes mAP/NDS
  is valid only when the data and tokens match the official NuScenes split.
- Train with `pred_velo=False` and `pred_attrs=False` only when the Karfic
  annotation contract cannot supply those targets; make that choice explicit
  in the config rather than hiding missing labels in the converter.

## Readiness gate

Karfic is ready for camera-only FCOS3D training when a read-only validator can
prove, for both train and validation splits:

```text
every image path exists
every sample and camera frame has a unique ID and timestamp
every camera has valid cam2img and cam2ego
every annotated object has a valid class, camera-frame box, center_2d, depth
all depths are positive and finite
all resized samples preserve centers_2d/cam2img consistency
the generated PKL loads through NuScenesDataset without fallback data
```
