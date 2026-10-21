# NuScenes camera-only MV-FCOS3D

Use `multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py` with
`../_base_/datasets/nuscenes-mv3d-10class.py`.

This is the MultiViewDfM integration, not the monocular FCOSMono3D head.
Six views at one timestamp are fused into a common 3D grid and BEV features.
No point-cloud input is loaded. The NuScenesVelocityAnchor3DHead predicts
9D boxes: x, y, z, dx, dy, dz, yaw, vx, vy. Velocity supervision is part of
loss_bbox; no separate monocular depth, centerness or attribute loss exists.

The baseline starts with batch size 1, 800x450 views and 12 vertical voxels.
Camera order is FRONT_LEFT, FRONT, FRONT_RIGHT, BACK_LEFT, BACK, BACK_RIGHT,
with each name prefixed CAM_. The dataset adapter validates and orders images
and their calibration. Do not rename ego2cam to lidar2cam for LiDAR-frame boxes.

## Authoritative guides

- [Installation](../../docs/project/installation.md)
- [PKL schema and camera ordering](../../docs/project/data-preparation.md)
- [Smoke check and full training commands](../../docs/project/training.md)
- [Evaluation and metrics](../../docs/project/evaluation.md)
- [Architecture and losses](../../docs/project/architecture.md)
- [Verification evidence](../../docs/project/validation.md)
- [Troubleshooting](../../docs/project/troubleshooting.md)

Use absolute annotation overrides for portability. Review the resolved config
rather than inferring runtime settings from the filename. A passing small CUDA
smoke check establishes execution, not trained accuracy or full-grid convergence.
Existing monocular workflows are separate and retain their own heads/configs.
