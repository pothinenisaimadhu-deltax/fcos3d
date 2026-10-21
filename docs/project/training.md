# Training, fine-tuning and continuation

## Select the workflow

| Model | Config |
| --- | --- |
| FCOS3D | configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py |
| PGD | configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py |
| Windows PGD wrapper | configs/pgd/pgd_mm3d_windows.py |
| MV-FCOS3D | configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py |
| Custom mono | configs/custom/fcos3d_custom_nuscenes_json.py or pgd_custom_nuscenes_json.py |

This fork's recipe files have local modifications; filenames are not a promise
of upstream-identical hyperparameters. Review the resolved config saved in
the work directory.

## Smoke check

```bash
python tools/check_mvfcos3d.py --data-root data/nuscenes --train-ann "$(pwd)/data/nuscenes_infos/nuscenes_infos_train.pkl" --val-ann "$(pwd)/data/nuscenes_infos/nuscenes_infos_val.pkl" --small
```

This checks a real training/backward pass, 9D prediction and one-sample subset
evaluation. It does not train an epoch, apply optimizer updates or save a
checkpoint. It uses random initialization without downloading backbone weights.
The small spatial grid and image size are not the full training recipe.

## Full MV training on Mini

Bash example:

```bash
datasetRoot="$(pwd)/data/nuscenes"
annotationRoot="$(pwd)/data/nuscenes_infos"
CUDA_VISIBLE_DEVICES=0 python tools/train.py \
  configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py \
  --work-dir work_dirs/mvfcos3d_mini \
  --cfg-options \
  "train_dataloader.dataset.data_root=$datasetRoot" \
  "train_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_train.pkl" \
  "val_dataloader.dataset.data_root=$datasetRoot" \
  "val_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_val.pkl" \
  "val_evaluator.data_root=$datasetRoot" \
  "val_evaluator.ann_file=$annotationRoot/nuscenes_infos_val.pkl"
```

**Important:** relative annotation paths in a dataset may be joined to its
data_root. In these examples supply absolute annotation paths via overrides,
or put the PKLs under the dataset root and use names relative to it. The
evaluator's annotation path is separately resolved. For portable shell use,
define an absolute annotation directory as shown below.

PowerShell example with absolute paths:

```powershell
$datasetRoot = (Resolve-Path "data/nuscenes").Path
$annotationRoot = (Resolve-Path "data/nuscenes_infos").Path
python tools/train.py configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py --work-dir work_dirs/mvfcos3d_mini --cfg-options "train_dataloader.dataset.data_root=$datasetRoot" "train_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_train.pkl" "val_dataloader.dataset.data_root=$datasetRoot" "val_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_val.pkl" "val_evaluator.data_root=$datasetRoot" "val_evaluator.ann_file=$annotationRoot/nuscenes_infos_val.pkl"
```

For Bash, use an absolute dataset root and annotation root as well. For
trainval, point at trainval PKLs. For intentional nonstandard scene subsets,
set `val_evaluator.eval_subset=True`; standard Mini uses the official mini_val
split and should not need that override.

## Mono FCOS3D and PGD

Use the same train/val dataset and evaluator path overrides with the mono
config. For Mini, add train and val
`dataset.metainfo.version=v1.0-mini`. On Windows add:

```text
env_cfg.mp_cfg.mp_start_method=spawn
train_dataloader.num_workers=0
train_dataloader.persistent_workers=False
val_dataloader.num_workers=0
val_dataloader.persistent_workers=False
```

The existing PGD recipe contains a generic mmdet.Resize step. Verify its
calibration/center handling for your exact pipeline before a geometry-sensitive
run; do not infer correctness from successful image loading alone. A documentation
update does not silently change that experimental recipe.

## Batch size and GPU memory

`train_dataloader.batch_size` is per process/GPU, not the camera count. MV
batch size 1 means six images. With ordinary distributed training, global
batch size is per-GPU batch times world size, before any gradient accumulation.

Start at 1 for MV. Full-resolution/grid training is larger than the smoke
test. Increase only after checking peak memory and throughput. Validation and
test batch sizes are independent. If changing voxel/grid sizes, check the 3D
neck and BEV axis order, not just memory.

## Optimizer and learning rate

The MV baseline uses AdamW, base LR 0.0005, backbone multiplier 0.1, gradient
clipping, a 500-iteration linear warmup and epoch milestones 20 and 27 in a
30-epoch loop. The logged group LR can differ from base_lr because of backbone
multipliers. Not every parameter group necessarily has the displayed LR.

For a **fresh** 30-epoch run with the requested decays after 5, 15 and 25
epochs, the conceptual schedule is:

```python
optim_wrapper = dict(optimizer=dict(lr=0.001))
param_scheduler = [
    dict(type='MultiStepLR', begin=0, end=30, by_epoch=True,
         milestones=[5, 15, 25], gamma=0.1)
]
train_cfg = dict(max_epochs=30)
```

Replace the scheduler list deliberately. This example omits warmup.
It gives 0.001, 0.0001, 0.00001 and 0.000001 at the successive stages for a
base group. A backbone multiplier of 0.1 gives ten times smaller LR for that
group. Confirm epoch-boundary behavior in the logs.

Do not change LR merely to force a displayed loss to fall. Compare validation
metrics, geometry checks and finite gradients. Mono LR defaults and PGD code
weights differ from MV; their losses are not directly comparable.

## Initialize versus resume

`load_from` initializes model weights for a new run; it does not restore the
previous optimizer, epoch and scheduler state. `--resume` restores the run.

```bash
python tools/train.py CONFIG --work-dir work_dirs/RUN --resume work_dirs/RUN/epoch_10.pth --cfg-options train_cfg.max_epochs=30
```

Ten completed epochs plus max_epochs=30 means twenty more, not thirty more.
If max_epochs equals the completed epoch count, the runner can exit immediately.
Include the original dataset path overrides when resuming.

The default MV recipe initializes the backbone from torchvision ImageNet.
It does not include a NuScenes-trained MV checkpoint. A monocular PGD
checkpoint is not a drop-in MV resume checkpoint. Backbone-only transfer
requires an explicit conversion/loading plan and inspection of mismatch logs.

Changing GPU count, batch size, optimizer or scheduler while resuming changes
the experiment. Restored state can override newly supplied LR values. Plan
and record such changes instead of assuming config edits take effect.

## Work directory and checkpoint selection

Keep each experiment in a unique directory. It contains logs, the resolved
config, resumable epoch checkpoints and best-checkpoint artifacts. Selection
by NDS can choose a different epoch than selection by mAP. Report the criterion.
Do not expose raw work directories publicly without reviewing paths and data.

Selective mono fine-tuning is available through `tools/finetune_fcos3d.py`
with checkpoint, freeze, freeze-epochs, batch-size and epochs options. Its
module-freezing assumptions are not automatically supported for MV.

A successful command is only the beginning: run a small no-augmentation
overfit check before expensive training if predictions remain misaligned.
