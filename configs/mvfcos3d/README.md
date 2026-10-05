# Camera-only NuScenes MV-FCOS3D in this checkout

This ports the reference repository's `MultiViewDfM` recipe and its separate
`NuScenesVelocityAnchor3DHead`. It is not the monocular FCOS3D head: it fuses
six camera feature maps into a 3D voxel grid and predicts BEV anchor boxes.
No point clouds are loaded. Boxes are 9D: x, y, z, dx, dy, dz, yaw, vx, vy.
Velocity is supervised inside `loss_bbox`; there is no attribute head or
separate monocular depth/centerness loss. Single-time multi-view input does
not directly observe motion across time.

## Requirements and data

Use the same working PyTorch/MMCV CUDA environment as the reference repo.
The Python environment may be reused, but launch from **this checkout**.
The custom imports are opt-in; existing monocular configs and converters
are not overwritten.

Use updated MMDetection3D v2 info PKLs with `data_list` and `metainfo`.
Each sample must include all six camera entries (`img_path`, `cam2img`,
`lidar2cam`), frame-level LiDAR-coordinate `instances`, and the standard
LiDAR-to-ego and ego-to-global metadata used by NuScenesMetric. Images are
loaded from `samples/<camera>/`; full absolute image paths also work.
An `ego2cam` matrix must NOT be renamed to `lidar2cam` for LiDAR-frame boxes.
The PKL metainfo version must match the JSON directory, e.g. `v1.0-mini`.
This adapter takes the version from the PKL instead of inheriting trainval.

Baseline training uses deterministic 800x450 resizing, original intrinsics
plus per-view scale factors for voxel projection, fixed camera ordering,
12 vertical voxels, and batch size 1. Additional crop/flip augmentation is
deliberately disabled until geometry and an overfit test have been checked.

## Local one-batch smoke test (PowerShell)

With your `mm3d` environment active, from `C:\Users\saimadhu-deltax\code\fcos3d`:

```powershell
python tools/check_mvfcos3d.py `
  --data-root C:/Users/saimadhu-deltax/Downloads/archive `
  --train-ann C:/Users/saimadhu-deltax/Downloads/minipkl/nuscenes_infos_train.pkl `
  --val-ann C:/Users/saimadhu-deltax/Downloads/minipkl/nuscenes_infos_val.pkl `
  --small
```

`--small` reduces images and the spatial grid **only inside this check**.
It checks one training/backward pass, 9D prediction, and one-sample subset
evaluation. It does not load pretrained weights, save a checkpoint, or give
a meaningful trained-model accuracy score. Source PKLs are unchanged.

## Train on your local NuScenes Mini

```powershell
python tools/train.py `
  configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py `
  --work-dir work_dirs/mvfcos3d_nuscenes_mini `
  --cfg-options `
  train_dataloader.dataset.data_root=C:/Users/saimadhu-deltax/Downloads/archive `
  train_dataloader.dataset.ann_file=C:/Users/saimadhu-deltax/Downloads/minipkl/nuscenes_infos_train.pkl `
  val_dataloader.dataset.data_root=C:/Users/saimadhu-deltax/Downloads/archive `
  val_dataloader.dataset.ann_file=C:/Users/saimadhu-deltax/Downloads/minipkl/nuscenes_infos_val.pkl `
  val_evaluator.data_root=C:/Users/saimadhu-deltax/Downloads/archive `
  val_evaluator.ann_file=C:/Users/saimadhu-deltax/Downloads/minipkl/nuscenes_infos_val.pkl
```

The full baseline is substantially larger than the small smoke check. Start
with batch size 1; a successful small test does not establish full-resolution
GPU memory capacity. For a server, use its Linux paths and Bash `\` line
continuations. Never put a space after an override's `=` or continuation.
For custom scene subsets, add `val_evaluator.eval_subset=True` only when
evaluation is intentionally against exactly the PKL tokens.

The default loads ImageNet ResNet101 backbone weights via torchvision, not
a NuScenes-trained MV checkpoint. The first run may need a download.
Do not resume a monocular PGD checkpoint into this architecture.
For a compatible MV checkpoint, use `load_from` to initialize a new run;
use `--resume path/to/epoch_N.pth` to restore optimizer and epoch state.
`train_cfg.max_epochs` is the total epoch limit, not additional epochs.

For evaluation with `tools/test.py`, override **test** dataloader root/ann
and **test** evaluator root/ann, then pass a compatible MV checkpoint.

## Verification

```powershell
python -m pytest tests/test_models/test_mvfcos3d_nuscenes.py -q
```

Tests cover config/entrypoint validation, Mini version and camera ordering,
9D training priors and velocity gradients, prediction priors, and a reduced
grid R101/DCNv2 loss/backward/predict cycle on CUDA. These prove execution,
not convergence or high NuScenes AP; verify GT alignment before a long run.
