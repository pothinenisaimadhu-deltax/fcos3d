# Architecture and code ownership

## End-to-end execution

```text
NuScenes images + metadata
  -> tools/create_data.py
  -> raw converter -> v2 updater -> dataset validation
  -> infos PKLs
  -> tools/train.py + resolved config
  -> dataset parser -> transforms -> data preprocessor
  -> detector -> head -> losses -> optimizer / scheduler
  -> checkpoint
  -> tools/test.py -> prediction formatting -> NuScenesMetric
```

MMEngine Runner owns loops, optimizer state, hooks, checkpoint lifecycle and
evaluation scheduling. It does not convert annotations or repair geometry.
Changing a runner is not a fix for incorrect calibration.

## Module map

| Responsibility | Main location |
| --- | --- |
| Dataset creation | tools/create_data.py |
| NuScenes geometry/info conversion | tools/dataset_converters/nuscenes_converter.py |
| V2 PKL schema conversion | tools/dataset_converters/update_infos_to_v2.py |
| Canonical camera order | tools/dataset_converters/nuscenes_camera_order.py |
| Dataset/projection validator | tools/validate_fcos3d_nuscenes.py |
| Mono dataset parsing | mmdet3d/datasets/nuscenes_dataset.py |
| MV order/calibration checks | mmdet3d/datasets/nuscenes_multiview_dataset.py |
| Opt-in MV registrations | mmdet3d/models/mvfcos3d.py |
| Multi-view feature/grid projection | mmdet3d/models/detectors/multiview_dfm.py |
| Voxel-to-BEV neck | mmdet3d/models/necks/imvoxel_neck.py |
| 9D MV head | mmdet3d/models/dense_heads/nuscenes_velocity_anchor3d_head.py |
| Box coder | mmdet3d/models/task_modules/coders/delta_xyzwhlr_bbox_coder.py |
| Prediction evaluation | mmdet3d/evaluation/metrics/nuscenes_metric.py |

## Monocular path

FCOSMono3D uses a ResNet/FPN image feature extractor and either FCOSMono3DHead
or PGDHead. Mono NuScenes loading generates one camera sample with its own
camera-frame annotations, calibration, projected centers and depths.

Typical FCOS3D terms include classification, offsets, depth, size, rotation,
centerness, velocity, direction and configured attributes. PGD can add
additional depth/2D regression terms. The exact loss dictionary depends on the
head configuration; logs should be interpreted from the actual implementation.

Code weights scale encoded regression coordinates. They are not class weights,
learning rates or accuracy targets. A small weighted velocity loss may coexist
with high real-unit AVE.

## MV path

```text
[B,6,3,H,W] images
  -> R101/DCNv2 + FPN per view
  -> project common voxel centers with original K and lidar2cam
  -> scale/crop/flip-aware feature sampling
  -> visible-view feature aggregation
  -> 3D voxel neck
  -> BEV feature [B,C,Ny,Nx]
  -> class / 9D regression / direction heads
```

The baseline has twelve vertical voxels. OutdoorImVoxelNeck reduces height
12 -> 6 -> 3 -> 1, then transposes the BEV spatial axes into the anchor head's
expected ordering. Changing height without checking convolution output sizes
can produce an assertion or kernel-size failure. Removing the assertion does
not make an incompatible grid correct.

The new head keeps the standard Anchor3DHead separate. It appends two zero
velocity dimensions to geometric priors in both target assignment and prediction
decoding. The nine-coordinate delta coder learns vx/vy along with geometry.
Zero **prior** velocity is not a zero **prediction** constraint.

## Why the MV log has three principal losses

| Term | What it represents |
| --- | --- |
| loss_cls | Anchor class prediction |
| loss_bbox | Encoded position, size, yaw and velocity regression |
| loss_dir | Direction-bin disambiguation |

There is no mono pixel-offset/depth branch, centerness branch or attribute
classifier in this MV head. Adding names to a logger does not create those
objectives. If separate velocity diagnostics are added later, avoid including
the same term twice in the optimized total.

The baseline uses one six-camera timestamp with num_ref_frames=-1. Velocity
can still be supervised from labels, but motion is not directly observed across
time. Temporal modeling is not implemented by merely increasing that config
value: it needs temporally grouped data and consistent cross-frame transforms.

## Isolation and extension

MV modules are imported through config custom_imports; mono configurations
do not need the MV path. Training/test guards accept specific supported
model/dataset pairs, not arbitrary upstream detectors.

New architectures need registrations, data contracts, head/coder compatibility,
prediction formatting and tests. A config file alone is not sufficient.
Do not change shared evaluators to mask incorrect annotations or convert ego
boxes into apparent LiDAR boxes by changing a class label.
