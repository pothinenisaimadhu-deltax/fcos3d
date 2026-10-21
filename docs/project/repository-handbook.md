# FCOS3D repository handbook

This handbook explains the file structure, model implementations, data contracts,
configuration, and commands in this DeltaX India MMDetection3D fork. It is intended
for someone opening the repository for the first time and for engineers running
experiments. Paths and defaults were inspected in this checkout on 2026-10-21.

The supported detector paths are **FCOS3D, PGD, and camera-only NuScenes
MV-FCOS3D**. The package is still named `mmdet3d`. Retained upstream tests,
Docker recipes, and documentation cover a wider toolbox than this fork supports.

Commands below are examples checked against local source and argument definitions.
They require the indicated dependencies, dataset, and compatible checkpoint;
documenting a command does not establish that a training run has completed.

## Contents

1. [Repository structure](#repository-structure)
2. [Important files and responsibilities](#important-files-and-responsibilities)
3. [Models and execution flow](#models-and-execution-flow)
4. [Configuration reference](#configuration-reference)
5. [Environment and installation](#environment-and-installation)
6. [Dataset layout and conversion](#dataset-layout-and-conversion)
7. [PowerShell command setup](#powershell-command-setup)
8. [Validation and smoke commands](#validation-and-smoke-commands)
9. [Training commands](#training-commands)
10. [Resume and fine-tuning](#resume-and-fine-tuning)
11. [Evaluation and prediction export](#evaluation-and-prediction-export)
12. [Inference and visualization](#inference-and-visualization)
13. [Linux and distributed commands](#linux-and-distributed-commands)
14. [Custom JSON data](#custom-json-data)
15. [Outputs and metrics](#outputs-and-metrics)
16. [Tests and troubleshooting](#tests-and-troubleshooting)
17. [Changing the repository](#changing-the-repository)

The companion [file inventory](file-inventory.md) lists every Git-indexed file
present when this documentation was generated. The tables below explain the
principal implementation files rather than assigning equal importance to every
inherited test or image asset.

## Repository structure

```text
fcos3d/
|-- README.md                  Project introduction and documentation links
|-- CONTRIBUTING.md            Contribution and verification expectations
|-- LICENSE / CITATION.cff     License and upstream attribution
|-- setup.py / setup.cfg       Python packaging and code style configuration
|-- requirements.txt           Includes build, optional, runtime, and test lists
|-- requirements/              Dependency groups, including documentation
|-- configs/
|   |-- _base_/
|   |   |-- datasets/          Mono and six-camera NuScenes pipelines/loaders
|   |   |-- models/            FCOS3D, PGD, and MultiViewDfM base definitions
|   |   |-- schedules/         Optimizer and loop templates
|   |   `-- default_runtime.py Hooks, logging, multiprocessing, default scope
|   |-- fcos3d/                FCOS3D baseline and fine-tuning recipes
|   |-- pgd/                   PGD baseline, fine-tuning, Windows wrapper
|   |-- mvfcos3d/              Ten-class six-camera velocity recipe
|   `-- custom/                Custom JSON mono templates
|-- mmdet3d/
|   |-- datasets/              Dataset parsing and image/annotation transforms
|   |-- models/                Detectors, heads, necks, coders, preprocessing
|   |-- evaluation/metrics/    NuScenes formatting and metric implementation
|   |-- engine/hooks/          Visualization and numerical diagnostics
|   |-- structures/            3D boxes, points, coordinate conversions, samples
|   |-- visualization/         Rendering helpers and local visualizer
|   |-- utils/                 Registration, environment, compatibility helpers
|   |-- registry.py            Model/dataset/metric registry definitions
|   `-- __init__.py            Framework version compatibility checks
|-- tools/                     Conversion, training, evaluation, validation
|-- demo/mono_det_demo.py       Retained demo; see inference limitations below
|-- tests/                     Focused fork tests and retained upstream tests
|-- docs/project/              Current project-specific documentation
|-- docs/en/                   Retained upstream framework documentation
|-- resources/                 Documentation figures and example images
|-- checkpoints/               Local mono pretrained checkpoint artifacts
|-- samplers/                  Existing local train/validation PKL artifacts
|-- work_dirs/                 Generated experiment artifacts
|-- docker/                    Retained image and serving recipes
|-- .github/ / .circleci/       Automation and contribution templates
`-- .dev_scripts/              Maintenance helpers
```

`data/` is an expected user-provided dataset location; it need not exist in a
fresh checkout. Checkpoints, local annotations, caches, and experiment outputs
are not guaranteed to be included in a clone. `samplers/` contains annotation
files; its name does not mean it implements the dataloader sampler algorithm.

## Important files and responsibilities

### Entry points

| File | Responsibility | Main inputs / result |
| --- | --- | --- |
| [tools/train.py](../../tools/train.py) | Loads config, merges overrides, validates supported model/dataset combinations, chooses NDS checkpoint key, starts MMEngine Runner | Config and optional resume checkpoint -> logs and trained checkpoints |
| [tools/test.py](../../tools/test.py) | Loads matching model/checkpoint and runs the test loop; optionally enables visualization | Config + checkpoint -> metrics and configured prediction artifacts |
| [tools/finetune_fcos3d.py](../../tools/finetune_fcos3d.py) | Adds selective freezing and optional unfreezing for mono fine-tuning | Config + checkpoint + freeze options -> a new fine-tuning run |
| [tools/create_data.py](../../tools/create_data.py) | Creates NuScenes infos, upgrades them to v2, and normally runs validation | Sensor root + JSON metadata -> train/val PKLs |
| [tools/check_mvfcos3d.py](../../tools/check_mvfcos3d.py) | Builds one real sample, runs finite loss/backward, 9D prediction, and one-sample subset evaluation | Dataset + PKLs + CUDA -> execution smoke result |
| [tools/validate_fcos3d_nuscenes.py](../../tools/validate_fcos3d_nuscenes.py) | Checks annotation fields, paths, geometry, metadata, and optional mono config/checkpoint | Data/annotation roots -> validation report or error |
| [tools/validate_custom_nuscenes_json.py](../../tools/validate_custom_nuscenes_json.py) | Validates a custom mono JSON manifest | JSON path, optional test mode -> schema check |
| [tools/stitch_nuscenes_cameras.py](../../tools/stitch_nuscenes_cameras.py) | Groups six camera images/renders into mosaics and video | Images + optional PKL grouping -> frames and MP4 |
| `tools/stich_backup.py` | Older stitching implementation retained under its original spelling | Historical reference; use the main stitch script for new commands |
| `tools/dist_train.sh`, `tools/dist_test.sh` | Bash wrappers around PyTorch distributed launch | Config, GPU count, optional overrides |
| `tools/slurm_train.sh`, `tools/slurm_test.sh` | Cluster submission helpers | Site-specific SLURM configuration required |
| `tools/create_data.sh` | Shell convenience script | Inspect local paths before using |

### Dataset, model, and metric implementation

| File | What to read or change here |
| --- | --- |
| `tools/dataset_converters/nuscenes_converter.py` | Raw NuScenes sensor/pose/annotation conversion and split handling |
| `tools/dataset_converters/update_infos_to_v2.py` | Conversion to `metainfo` + `data_list`, including per-camera records |
| `tools/dataset_converters/nuscenes_camera_order.py` | Shared six-camera order |
| `mmdet3d/datasets/det3d_dataset.py` | Common dataset loading and box/annotation handling |
| `mmdet3d/datasets/nuscenes_dataset.py` | NuScenes mono/frame parsing and annotation conversion |
| `mmdet3d/datasets/nuscenes_multiview_dataset.py` | Enforces camera/calibration pairing and reads version from PKL metainfo |
| `mmdet3d/datasets/nuscenes_json_dataset.py` | Validates/loads NuScenes-style JSON for mono workflows |
| `mmdet3d/datasets/transforms/loading.py` | Image, multi-view image, and annotation loading |
| `mmdet3d/datasets/transforms/transforms_3d.py` | `Resize3D`, `RandomResize3D`, `MultiViewWrapper`, flips, and filters |
| `mmdet3d/datasets/transforms/formating.py` | `Pack3DDetInputs`; spelling is the actual filename |
| `mmdet3d/models/data_preprocessors/data_preprocessor.py` | Normalization, padding, batching, and model input preparation |
| `mmdet3d/models/detectors/single_stage_mono3d.py` | Shared mono feature extraction and loss/prediction structure |
| `mmdet3d/models/detectors/fcos_mono3d.py` | `FCOSMono3D` detector used by both FCOS3D and PGD |
| `mmdet3d/models/dense_heads/fcos_mono3d_head.py` | FCOS3D target assignment, branch losses, and decoding |
| `mmdet3d/models/dense_heads/pgd_head.py` | PGD extensions to the FCOS3D head, including depth/2D branches |
| `mmdet3d/models/mvfcos3d.py` | Opt-in registration of MV dataset, transforms, detector, neck, and 9D head |
| `mmdet3d/models/detectors/dfm.py` | Base detector machinery used by MultiViewDfM |
| `mmdet3d/models/detectors/multiview_dfm.py` | Multi-camera feature projection/aggregation and common-frame prediction |
| `mmdet3d/models/layers/fusion_layers/point_fusion.py` | Projection-aware image feature sampling |
| `mmdet3d/models/necks/imvoxel_neck.py` | `OutdoorImVoxelNeck`, converts voxel features to BEV features |
| `mmdet3d/models/dense_heads/anchor3d_head.py` | Shared anchor-based classification, box, and direction machinery |
| `mmdet3d/models/dense_heads/nuscenes_velocity_anchor3d_head.py` | Extends geometric anchor priors with velocity dimensions for training and prediction |
| `mmdet3d/models/task_modules/coders/fcos3d_bbox_coder.py` | FCOS3D box decoding |
| `mmdet3d/models/task_modules/coders/pgd_bbox_coder.py` | PGD box/depth decoding |
| `mmdet3d/models/task_modules/coders/delta_xyzwhlr_bbox_coder.py` | Delta encoding/decoding, configured with nine coordinates for MV |
| `mmdet3d/models/task_modules/anchor/anchor_3d_generator.py` | Anchor/grid generation |
| `mmdet3d/models/task_modules/assigners/max_3d_iou_assigner.py` | IoU-based MV anchor assignment |
| `mmdet3d/evaluation/metrics/nuscenes_metric.py` | Prediction formatting, official/subset scoring, car-only protocol |
| `mmdet3d/engine/hooks/numerical_debug_hook.py` | Numerical debugging hooks, used by the PGD fine-tuning recipe |
| `mmdet3d/engine/hooks/visualization_hook.py` | Test-time drawing hook |
| `mmdet3d/visualization/local_visualizer.py` | Box/image rendering |
| `mmdet3d/structures/bbox_3d/` | Camera/LiDAR/depth box types, coordinate modes, and projection helpers |
| `mmdet3d/utils/setup_env.py` | Registers standard modules and establishes the package scope |

Backbone and FPN types prefixed `mmdet.` are supplied by MMDetection. Their full
implementations are not duplicated in this repository. `__init__.py` files export
symbols or register modules; directory presence alone does not register a type.

## Models and execution flow

### Model comparison

| Property | FCOS3D | PGD | NuScenes MV-FCOS3D |
| --- | --- | --- | --- |
| Detector | `FCOSMono3D` | `FCOSMono3D` | `MultiViewDfM` |
| Main head | `FCOSMono3DHead` | `PGDHead` | `NuScenesVelocityAnchor3DHead` |
| Input per sample | One camera image | One camera image | Six camera images at one timestamp |
| Dataset | `NuScenesDataset` or custom JSON | Same mono choices | `NuScenesMultiViewDataset` |
| Loading mode | `mv_image_based` | `mv_image_based` | `frame_based` |
| Target/output box frame | Camera | Camera | LiDAR coordinate frame |
| Detection approach | Anchor-free image features | Anchor-free with depth extensions | Project image features to a common voxel grid, then anchor-based BEV detection |
| Velocity | Configured mono velocity branch | Configured mono velocity branch | Nine-dimensional regression including `vx`, `vy` |
| Attributes | Configured learned attribute branch | Configured learned attribute branch | No learned attribute branch; formatter derives/defaults attributes |

`mv_image_based` expands a frame into separate monocular samples. It does not
mean the mono detector jointly fuses six images. For MV, batch size 1 represents
six images. All three supported paths use images as detector input; calibration
and LiDAR-frame ground truth do not constitute LiDAR point-cloud input.

### Training and evaluation flow

```text
Raw images + NuScenes JSON + calibration/poses
  -> create_data.py -> raw converter -> v2 updater -> validator
  -> annotation PKLs
  -> train.py + resolved config
  -> dataset -> transforms -> Pack3DDetInputs -> data preprocessor
  -> model -> head losses -> backward -> optimizer/scheduler -> checkpoint
  -> test.py + same architecture/preprocessing -> prediction formatting
  -> NuScenesMetric -> metrics and optional JSON/rendered results
```

MMEngine Runner owns loops, hooks, optimization, logging, and checkpoint state.
The config chooses components through registries.

### Mono architecture and losses

The supplied R101 recipes extract ResNet-101/DCNv2 features and combine them
with FPN. FCOS3D predicts classification, image-plane offset, depth, size,
rotation, velocity, direction, centerness, and configured attributes. PGD extends
the mono head with probabilistic/geometric depth machinery and optional 2D box
regression. Read the actual head and resolved config for enabled loss terms.

### MV architecture and losses

```text
[B, 6, 3, H, W]
  -> per-camera ResNet-101/DCNv2 and FPN
  -> project common voxel centers into calibrated camera views
  -> sample features using original intrinsics and resize/crop/flip metadata
  -> combine visible-view features
  -> OutdoorImVoxelNeck -> BEV
  -> class + 9D box + direction outputs
```

The recipe spans `x,y = [-50,50]` meters and `z = [-5,3]` meters, with voxel
size `(0.5,0.5,8/12)`: nominally 200 x 200 x 12 cells. The neck reduces vertical
height `12 -> 6 -> 3 -> 1`. Changing vertical resolution requires checking neck
convolution dimensions and BEV axis order.

MV reports `loss_cls`, `loss_bbox`, and `loss_dir`. `loss_bbox` includes
position, dimensions, yaw, and velocity; the last two regression code weights
are 0.2. The head pads 7D geometric priors with zero velocity in both assignment
and prediction. Zero prior velocity does not force predictions to zero.

`num_ref_frames=-1` uses one timestamp. Temporal motion input is not enabled by
the six-camera setting. A temporal extension requires dataset and transform work.

## Configuration reference

### Recipe map

| Recipe path under `configs/` | Purpose |
| --- | --- |
| `fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py` | Main ten-class FCOS3D recipe |
| `fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d_finetune.py` | FCOS3D second stage; supply a baseline checkpoint |
| `pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py` | PGD recipe |
| `pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d_finetune.py` | PGD numerical debugging/fine-tuning recipe; has a local checkpoint default |
| `pgd/pgd_mm3d_windows.py` | PGD wrapper using spawn, batch 1, zero workers |
| `mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py` | Six-camera NuScenes MV with 9D velocity |
| `custom/fcos3d_custom_nuscenes_json.py` | Custom JSON FCOS3D template |
| `custom/pgd_custom_nuscenes_json.py` | Custom JSON PGD template |

### Defaults in the current main recipes

| Setting | FCOS3D | PGD | MV-FCOS3D |
| --- | --- | --- | --- |
| Per-process training batch | 16 | 2 | 1 |
| Train workers | 4 | 2 | 2 |
| Epochs | 12 | 12 | 30 |
| Validation interval, epochs | 2 | 4 | 2 |
| Optimizer | SGD | SGD | AdamW |
| Base learning rate | 0.000025 | 0.004 | 0.0005 |
| Weight decay | 0.0001 | 0.0001 | 0.0001 |
| Warmup | 500 iterations, factor 1/3 | 500 iterations, factor 1/3 | 500 iterations, factor 1/3 |
| Epoch LR milestones | 8, 11 | 8, 11 | 20, 27 |
| Milestone multiplier | 0.1 | 0.1 | 0.1 |
| Train resize | 1600 x 900, keep ratio | 1600 x 900, generic resize | 800 x 450, keep ratio |
| Test resize | 1600 x 900 | Scale factor 1.0 | 800 x 450 |
| Multiprocessing | Inherited fork | Inherited fork | Spawn |

These are config values, not measured best settings. The Windows PGD wrapper
sets LR to `0.004/32 = 0.000125`. Mono uses bias LR multiplier 2; MV uses a
backbone LR multiplier of 0.1. Logged parameter-group LR may differ from base LR.
The FCOS3D fine-tuning file sets LR 0.001, which is higher than the current
baseline 0.000025 despite its inherited comment about halving LR.

The PGD training recipe uses `mmdet.Resize`, while FCOS3D uses `Resize3D`.
Check PGD centers/intrinsics and train/test image scaling on your data before
claiming geometry is correct. No preprocessing change is made by this handbook.

### How inheritance and overrides work

`_base_` loads dataset, model, schedule, and runtime definitions. Child dictionaries
merge into those bases; child lists generally replace corresponding lists.
`--cfg-options dotted.key=value` overrides the resulting config at launch.
Changing a top-level `data_root` variable after dictionaries are constructed
does not automatically rewrite every nested dataset/evaluator path.

| Key | Meaning |
| --- | --- |
| `train_dataloader.dataset.data_root` | Root for training images/metadata |
| `train_dataloader.dataset.ann_file` | Training annotation path |
| `val_dataloader.dataset.*` | Validation input paths/metadata |
| `test_dataloader.dataset.*` | Test input paths/metadata |
| `val_evaluator.*`, `test_evaluator.*` | Separate evaluator paths/options |
| `train_dataloader.batch_size` | Samples per GPU/process |
| `num_workers`, `persistent_workers` | Worker process settings; use false persistence for zero workers |
| `train_cfg.max_epochs` | Total epoch target, including completed epochs on resume |
| `optim_wrapper.optimizer.lr` | Base LR, subject to parameter groups and schedules |
| `load_from` | Weights initialization for a new experiment |
| `--resume [CHECKPOINT]` | Restore model, optimizer, scheduler, and progress |
| `default_hooks.checkpoint` | Save interval, retention, best-metric selection |
| `model.test_cfg` | Prediction thresholds/NMS; inspect model-specific keys |

Filename tokens such as `8xb2`, `16xb2`, and `1x` are recipe labels. They do not
override runtime batch size or epochs. Keep the saved resolved config with results.

## Environment and installation

Use an isolated Python environment with compatible CUDA-enabled PyTorch and
compiled MMCV operators. Python/PyTorch/CUDA wheel selection is platform-specific;
this repository does not provide a universally validated dependency lockfile.

`mmdet3d/__init__.py` enforces these ranges:

| Package | Required range |
| --- | --- |
| MMCV | `>=2.0.0rc4,<2.2.0` |
| MMEngine | `>=0.8.0,<1.0.0` |
| MMDetection | `>=3.0.0rc5,<3.4.0` |

Install compatible PyTorch first. Then run in the activated environment:

```powershell
python -m pip install -U openmim
mim install "mmengine>=0.8.0,<1.0.0"
mim install "mmcv>=2.0.0rc4,<2.2.0"
mim install "mmdet>=3.0.0rc5,<3.4.0"
python -m pip install -v -e .
python -m pip install pytest
python -m pip check
```

`requirements/runtime.txt` lists the dataset/geometry runtime dependencies;
`requirements/mminstall.txt` describes framework dependencies. Other lists cover
build, optional, test, and documentation packages. `mmcv-lite` is insufficient
for R101/DCNv2 and rotated-NMS execution.

```powershell
python -c "import torch, mmcv, mmengine, mmdet, mmdet3d; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(mmcv.__version__, mmengine.__version__, mmdet.__version__); print(mmdet3d.__file__)"
python -c "from mmcv.ops import ModulatedDeformConv2dPack, nms_rotated; print('Compiled operators imported')"
nvidia-smi
```

Verify the imported `mmdet3d` path belongs to this checkout, especially if another
fork was installed in editable mode. Successful imports do not prove a complete
training or operator execution path. See [installation](installation.md).

## Dataset layout and conversion

```text
data/
|-- nuscenes/
|   |-- samples/CAM_FRONT_LEFT/ ... other five camera folders
|   |-- samples/LIDAR_TOP/          Converter availability checks may use it
|   |-- sweeps/                    For generated sweep metadata
|   |-- maps/
|   `-- v1.0-mini/                  JSON tables, or v1.0-trainval/
`-- nuscenes_infos/
    |-- nuscenes_infos_train.pkl
    `-- nuscenes_infos_val.pkl
```

The conversion root contains the metadata version folder. Do not pass the JSON
folder itself as the dataset root. These examples create annotations in a
separate directory. Use a new output directory when regenerating an experiment's
PKLs, since existing filenames can be overwritten.

Mini conversion, run from repository root:

```powershell
python -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/nuscenes_infos --extra-tag nuscenes --version v1.0-mini
```

Full trainval conversion, with the matching trainval dataset installed:

```powershell
python -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/nuscenes_infos_trainval --extra-tag nuscenes --version v1.0
```

The `v1.0` entrypoint selects trainval and conditionally processes test metadata
when available. Mini must explicitly use `v1.0-mini`. Use module invocation
`python -m tools.create_data` so its `tools.*` imports resolve from the root.

| Conversion option | Purpose |
| --- | --- |
| `--max-sweeps` | Maximum sweep metadata count; default 10 |
| `--split-json` | Explicit custom train/validation scene split |
| `--nuscenes-path` | Alternate sensor/metadata root |
| `--trainval-meta-root` | Alternate metadata base |
| `--expected-train-samples`, `--expected-val-samples` | Expected conversion/validation counts |
| `--skip-validation` | Skip automatic validator; this does not verify correctness |

### Annotation contract

```text
metainfo: categories, dataset/info_version, version
data_list[]:
  sample_idx, token, timestamp, ego2global
  lidar_points.lidar2ego
  images[CAM_*]: img_path, cam2img, cam2ego, lidar2cam, timestamps/tokens
  instances[]: common-frame GT boxes, labels, velocity, validity metadata
  cam_instances[CAM_*][]: camera-frame boxes, 2D boxes, center, depth, attributes
```

The canonical camera order is:

```text
CAM_FRONT_LEFT, CAM_FRONT, CAM_FRONT_RIGHT,
CAM_BACK_LEFT, CAM_BACK, CAM_BACK_RIGHT
```

Keep image identity and calibration paired when reordering. Mono consumes
per-camera annotations; MV consumes common LiDAR-frame annotations and six views.
For column vectors at a shared ego pose, `lidar2cam = inverse(cam2ego) @ lidar2ego`.
Asynchronous poses require the corresponding ego/global composition.

Resize must keep image pixels, intrinsics, centers, and feature projection in a
consistent coordinate system. The MV recipe uses original intrinsics plus resize
metadata. Do not rescale both the intrinsic matrix and projection again. Inspect
full box corners, yaw, and dimensions across all cameras, not only center points.
See [data preparation](data-preparation.md) for additional geometry details.

## PowerShell command setup

Run all following PowerShell examples in the repository root, in the same shell
session. Replace the dataset location if yours differs. `Resolve-Path` requires
the files to exist, so complete conversion first.

```powershell
$datasetRoot = (Resolve-Path 'data/nuscenes').Path.Replace('\', '/')
$annotationRoot = (Resolve-Path 'data/nuscenes_infos').Path.Replace('\', '/')
$trainAnn = "$annotationRoot/nuscenes_infos_train.pkl"
$valAnn = "$annotationRoot/nuscenes_infos_val.pkl"
$fcosConfig = 'configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py'
$pgdConfig = 'configs/pgd/pgd_mm3d_windows.py'
$mvConfig = 'configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py'

# Applied during training, including its validation stage.
$trainPaths = @(
  "train_dataloader.dataset.data_root=$datasetRoot"
  "train_dataloader.dataset.ann_file=$trainAnn"
  "val_dataloader.dataset.data_root=$datasetRoot"
  "val_dataloader.dataset.ann_file=$valAnn"
  "val_evaluator.data_root=$datasetRoot"
  "val_evaluator.ann_file=$valAnn"
)
$testPaths = @(
  "test_dataloader.dataset.data_root=$datasetRoot"
  "test_dataloader.dataset.ann_file=$valAnn"
  "test_evaluator.data_root=$datasetRoot"
  "test_evaluator.ann_file=$valAnn"
)
$windowsTrain = @(
  'env_cfg.mp_cfg.mp_start_method=spawn'
  'train_dataloader.num_workers=0'
  'train_dataloader.persistent_workers=False'
  'val_dataloader.num_workers=0'
  'val_dataloader.persistent_workers=False'
)
$windowsTest = @(
  'env_cfg.mp_cfg.mp_start_method=spawn'
  'test_dataloader.num_workers=0'
  'test_dataloader.persistent_workers=False'
)
$monoMiniTrain = @(
  'train_dataloader.dataset.metainfo.version=v1.0-mini'
  'val_dataloader.dataset.metainfo.version=v1.0-mini'
)
$monoMiniTest = @('test_dataloader.dataset.metainfo.version=v1.0-mini')
```

`@trainPaths` is PowerShell array splatting: each array item becomes a separate
argument. Paths use forward slashes to avoid escape ambiguities. Keep every
override in one `key=value` argument with no space around `=`. For trainval,
change the annotation directory and replace mono Mini versions with
`v1.0-trainval`. MV reads version from its annotation metadata.

## Validation and smoke commands

Check converted mono data before training:

```powershell
python tools/validate_fcos3d_nuscenes.py --data-root $datasetRoot --ann-root $annotationRoot --metadata-root "$datasetRoot/v1.0-mini"
```

Optional validator arguments include `--config`, `--checkpoint`, expected sample
counts, and `--projection-tolerance` (default 0.1). Its config validation is
mono-specific; use the MV smoke helper for the multi-view model.

```powershell
python tools/check_mvfcos3d.py --data-root $datasetRoot --train-ann $trainAnn --val-ann $valAnn --small
```

The MV helper requires CUDA. `--small` uses 320 x 180 images, a reduced XY grid,
and lower pre-NMS candidate count. It disables backbone weight downloads, runs
loss/backward, verifies finite 9D predictions, and evaluates one validation
sample using a temporary subset PKL. It does not call an optimizer step or save
a checkpoint. Its AP/NDS are not trained-model accuracy.

## Training commands

### FCOS3D on Mini

```powershell
python tools/train.py $fcosConfig --work-dir work_dirs/fcos3d_mini --cfg-options @trainPaths @windowsTrain @monoMiniTrain train_dataloader.batch_size=1
```

Batch 1 is an explicit starter override; the recipe default is 16. This command
retains the configured LR and schedule. Choose and record your batch/LR policy
before treating a run as a benchmark reproduction.

### PGD on Mini

```powershell
python tools/train.py $pgdConfig --work-dir work_dirs/pgd_mini --cfg-options @trainPaths @windowsTrain @monoMiniTrain
```

The Windows wrapper already uses batch 1 and LR 0.000125. The generic resize
behavior described above still needs verification on the intended dataset.

### MV-FCOS3D on Mini

```powershell
python tools/train.py $mvConfig --work-dir work_dirs/mvfcos3d_mini --cfg-options @trainPaths @windowsTrain
```

This uses the full MV recipe rather than the reduced smoke grid. Default batch
is one six-camera sample. Memory use is substantially different from `--small`.
The backbone initializes from `torchvision://resnet101`, which can download
weights if not cached. No NuScenes-trained MV checkpoint is supplied by this
recipe.

### One-epoch execution run

```powershell
python tools/train.py $mvConfig --work-dir work_dirs/mvfcos3d_mini_1epoch --cfg-options @trainPaths @windowsTrain train_cfg.max_epochs=1 train_cfg.val_interval=1
```

This runs one full epoch of the provided training split and validates it. It
does not restrict training to one batch. A one-epoch result verifies execution
and checkpoint production, not convergence.

### Useful training arguments

| Argument | Behavior |
| --- | --- |
| `--work-dir PATH` | Explicit experiment directory; takes precedence over config |
| `--amp` | Switches an `OptimWrapper` to dynamic-loss-scale AMP |
| `--resume [PATH]` | Restore explicit checkpoint or auto-resume from work directory |
| `--cfg-options KEY=VALUE ...` | Merge config changes before Runner construction |
| `--auto-scale-lr` | Enables scaling if config has required auto-scale fields |
| `--sync_bn none/torch/mmcv` | Select SyncBN conversion |
| `--launcher none/pytorch/slurm/mpi` | Choose launcher |
| `--ceph` | Optional configured remote storage backend |

For GPU selection in PowerShell, set `$env:CUDA_VISIBLE_DEVICES = '0'` before
launching. The exposed physical GPU becomes logical device 0 in that process.

## Resume and fine-tuning

Continue the same MV experiment from an existing checkpoint:

```powershell
python tools/train.py $mvConfig --work-dir work_dirs/mvfcos3d_mini --resume work_dirs/mvfcos3d_mini/epoch_10.pth --cfg-options @trainPaths @windowsTrain train_cfg.max_epochs=30
```

Replace the checkpoint with an existing file. Ten completed epochs with total
target 30 means twenty more epochs. Keep original data, batch, and scheduling
settings when continuing the same experiment. Restored optimizer/scheduler
state can affect newly specified LR values.

For a new mono experiment initialized from a compatible baseline checkpoint:

```powershell
$baselineCheckpoint = 'work_dirs/fcos3d_mini/epoch_12.pth'
python tools/train.py $fcosConfig --work-dir work_dirs/fcos3d_transfer --cfg-options @trainPaths @windowsTrain @monoMiniTrain train_dataloader.batch_size=1 "load_from=$baselineCheckpoint"
```

Selective mono fine-tuning:

```powershell
python -m tools.finetune_fcos3d $fcosConfig --checkpoint $baselineCheckpoint --work-dir work_dirs/fcos3d_freeze --freeze backbone --freeze-epochs 2 --backbone-lr-mult 0.1 --batch-size 1 --epochs 12 --cfg-options @trainPaths @windowsTrain @monoMiniTrain
```

`--freeze-epochs 0` freezes selected modules for the whole run. A positive value
unfreezes after that many epochs. `--freeze` accepts comma-separated module names
such as `backbone` or `backbone.layer4`. Module invocation keeps this checkout
on the import path. This launcher is documented for mono module layouts.

The separate `_finetune.py` recipes change loss weights/LR and sometimes debug
hooks; they are not aliases for resume. Inspect their actual values and override
local `load_from` defaults. A PGD/FCOS3D checkpoint is not a compatible MV resume
checkpoint. Check mismatch logs when transferring any partial weights.

## Evaluation and prediction export

Use the matching architecture, classes, preprocessing, and dataset protocol.
These examples assume the named checkpoints have been produced; change them to
the actual selected checkpoint.

```powershell
python tools/test.py $fcosConfig work_dirs/fcos3d_mini/epoch_12.pth --work-dir work_dirs/fcos3d_mini_eval --cfg-options @testPaths @windowsTest @monoMiniTest
python tools/test.py $pgdConfig work_dirs/pgd_mini/epoch_12.pth --work-dir work_dirs/pgd_mini_eval --cfg-options @testPaths @windowsTest @monoMiniTest
python tools/test.py $mvConfig work_dirs/mvfcos3d_mini/epoch_30.pth --work-dir work_dirs/mvfcos3d_mini_eval --cfg-options @testPaths @windowsTest
```

For persistent NuScenes-format prediction output:

```powershell
python tools/test.py $mvConfig work_dirs/mvfcos3d_mini/epoch_30.pth --work-dir work_dirs/mvfcos3d_mini_export --cfg-options @testPaths @windowsTest test_evaluator.jsonfile_prefix=work_dirs/mvfcos3d_mini_export/predictions
```

Without a persistent prefix, the evaluator can use temporary JSON output.
Prediction JSON generation and scoring are separate operations within the
evaluation path. Test/validation paths must be overridden independently.

For an intentional custom scene subset, add
`test_evaluator.eval_subset=True`. This changes the protocol to the PKL token
set and requires matching prediction coverage. Official Mini uses `mini_val`;
official trainval uses `val`. Do not use subset mode to label a partial run as
official full validation.

## Inference and visualization

### Current single-image demo limitation

`demo/mono_det_demo.py` declares this interface:

```text
python demo/mono_det_demo.py IMAGE INFOS CONFIG CHECKPOINT [--device cuda:0] [--out-dir outputs]
```

However, it imports `mmdet3d.apis.MonoDet3DInferencer`, and this checkout has no
`mmdet3d/apis/` package. The demo is therefore a retained interface example,
not a working standalone inference command in this fork. Its `--cam-type`
argument is also removed from the parsed dictionary without forwarding it.
Do not rely on that flag to select camera calibration.

Use `tools/test.py` with a compatible annotation dataset and checkpoint for
the implemented prediction path. A bare image is insufficient for calibrated
3D box prediction; the model also needs its intrinsics and expected metadata.
Repairing or adding a standalone inference API would be a separate code change.

### Mono prediction renders

The mono base config defines a visualizer and default visualization hook:

```powershell
python tools/test.py $fcosConfig work_dirs/fcos3d_mini/epoch_12.pth --work-dir work_dirs/fcos3d_mini_visuals --show-dir rendered --task mono_det --score-thr 0.3 --cfg-options @testPaths @windowsTest @monoMiniTest
```

The script describes `--show-dir` output under the work directory/timestamp.
Use logs to locate the actual generated path. `--score-thr` controls drawing;
prediction filtering/NMS lives in model config. `--show` requests interactive
display and is unnecessary for saving images.

The MV CLI accepts `--task multi-view_det`, but its base configs do not define
the same explicit `visualizer` block as the mono dataset. Verify/add the required
visualizer configuration and check six-camera output before relying on MV
rendering. This handbook does not claim the visualization path was runtime-tested.

### Camera mosaics and video

For already-rendered six-camera images, replace the input path with the real
visualization directory:

```powershell
python tools/stitch_nuscenes_cameras.py --input-root work_dirs/fcos3d_mini_visuals/rendered --ann-file $valAnn --output-dir work_dirs/fcos3d_mini_visuals/mosaic --image-kind 3d --fps 10 --width 640 --height 360
```

PKL grouping pairs camera filenames by sample. Missing views can skip a group.
Without PKL grouping, timestamp/sequence matching depends on available filenames;
verify alignment and frame counts. `--max-frames` limits output.
`--clean-output` removes previous generated outputs in the destination, so use
a dedicated generated directory. OpenCV video writer/codec support is required.

## Linux and distributed commands

Bash uses `$name` variables and backslash continuations; PowerShell uses array
splatting and backticks. The following is a self-contained Linux MV example:

```bash
datasetRoot="$(pwd)/data/nuscenes"
annotationRoot="$(pwd)/data/nuscenes_infos"
mvConfig="configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py"
trainPaths=(
  "train_dataloader.dataset.data_root=$datasetRoot"
  "train_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_train.pkl"
  "val_dataloader.dataset.data_root=$datasetRoot"
  "val_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_val.pkl"
  "val_evaluator.data_root=$datasetRoot"
  "val_evaluator.ann_file=$annotationRoot/nuscenes_infos_val.pkl"
)
CUDA_VISIBLE_DEVICES=0 python tools/train.py "$mvConfig" \
  --work-dir work_dirs/mvfcos3d_mini_linux --cfg-options "${trainPaths[@]}"
```

Two-GPU training using the provided wrapper, after defining the Bash variables:

```bash
CUDA_VISIBLE_DEVICES=0,1 bash tools/dist_train.sh "$mvConfig" 2 \
  --work-dir work_dirs/mvfcos3d_mini_2gpu --cfg-options "${trainPaths[@]}"
```

Two-GPU evaluation:

```bash
CUDA_VISIBLE_DEVICES=0,1 bash tools/dist_test.sh "$mvConfig" \
  work_dirs/mvfcos3d_mini_2gpu/epoch_30.pth 2 \
  --work-dir work_dirs/mvfcos3d_mini_2gpu_eval --cfg-options \
  "test_dataloader.dataset.data_root=$datasetRoot" \
  "test_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_val.pkl" \
  "test_evaluator.data_root=$datasetRoot" \
  "test_evaluator.ann_file=$annotationRoot/nuscenes_infos_val.pkl"
```

Wrappers use `torch.distributed.launch` and accept `NNODES`, `NODE_RANK`,
`MASTER_ADDR`, and `PORT`. They are Linux/Bash examples, not native PowerShell
scripts. The inherited distributed backend is NCCL. Configure launch/network
settings for your cluster. Per-GPU batch x GPU count gives global batch before
accumulation; LR does not automatically scale unless deliberately enabled.

## Custom JSON data

Start with [the custom data contract](../fcos3d_custom_nuscenes_data_requirements.md).
The JSON adapter accepts `data_list`, legacy `infos`, or a record list. Each
record needs `sample_idx`, `token`, and nonempty `images`; each image needs
`img_path`, `height`, `width`, and `cam2img`. Training also requires `ego2global`
and per-camera `cam_instances` with appropriate mono labels/targets.

```powershell
python -m tools.validate_custom_nuscenes_json data/custom/custom_train.json
python -m tools.validate_custom_nuscenes_json data/custom/custom_val.json --test-mode
```

The custom config files are **templates**. The FCOS3D template's `DumpResults`
evaluator changes type through a dictionary merge, so inherited NuScenes evaluator
fields must be removed before use. Its inherited best-NDS hook must also be disabled
when validation only exports predictions. For example, create an experiment
config `configs/custom/my_custom_fcos3d.py` containing:

```python
_base_ = './fcos3d_custom_nuscenes_json.py'
val_evaluator = dict(
    _delete_=True, type='DumpResults',
    out_file_path='work_dirs/my_custom_fcos3d/val_predictions.pkl')
test_evaluator = dict(
    _delete_=True, type='DumpResults',
    out_file_path='work_dirs/my_custom_fcos3d/test_predictions.pkl')
default_hooks = dict(checkpoint=dict(save_best=None))
```

Then, after creating valid manifests and verifying image prefixes:

```powershell
$customRoot = (Resolve-Path 'data/custom').Path.Replace('\', '/')
python tools/train.py configs/custom/my_custom_fcos3d.py --work-dir work_dirs/my_custom_fcos3d --cfg-options @windowsTrain train_dataloader.batch_size=1 "train_dataloader.dataset.data_root=$customRoot" "train_dataloader.dataset.ann_file=$customRoot/custom_train.json" "val_dataloader.dataset.data_root=$customRoot" "val_dataloader.dataset.ann_file=$customRoot/custom_val.json"
```

The example experiment config is a snippet to create, not an added repository
file. `DumpResults` exports predictions and supplies no NuScenes AP/NDS score.
The PGD custom template instead uses `NuScenesMetric` with `eval_subset=True`,
a persistent JSON prefix, and numerical debugging hooks. It requires compatible
NuScenes metadata, GT, and sample tokens; a schema-valid JSON manifest alone
does not establish that evaluation can run. Scoring custom data requires an
explicit compatible GT and metric protocol.
Custom six-camera fusion also needs common-frame GT and transforms; switching
the mono JSON dataset name alone does not implement that workflow.

## Outputs and metrics

Typical artifacts depend on the configured hooks and MMEngine version:

```text
work_dirs/RUN/
  <resolved-config>.py
  <timestamp>/                 Logs, scalar/visualization artifacts as configured
  epoch_N.pth                  Retained epoch checkpoints
  last_checkpoint              Pointer used for automatic resume
  best_<metric>_epoch_N.pth    When save_best is enabled and the metric exists
```

FCOS3D/MV recipes retain at most three ordinary epoch checkpoints and select best
NDS at validation intervals. Best-checkpoint names are generated and should not
be guessed. PGD baseline inherits checkpoint interval -1, disabling ordinary
periodic saves; the checkpoint hook's default `save_last=True` still saves the
final epoch. Configure a positive interval if intermediate resumable checkpoints
are needed.
An example epoch path in this guide is not evidence that the file exists.

| Metric | Meaning | Preferred direction |
| --- | --- | --- |
| mAP | NuScenes detection AP averaged across classes/center-distance thresholds | Higher |
| NDS | Composite detection and true-positive quality score | Higher |
| mATE | Translation error, meters | Lower |
| mASE | Scale error | Lower |
| mAOE | Orientation error, radians | Lower |
| mAVE | Velocity error, meters/second | Lower |
| mAAE | Attribute error | Lower |

These are detection metrics, not ordinary classification accuracy. Compare
models only with matching splits, class sets, conversion, evaluator, and checkpoint
selection rules. Car-only, Mini, custom subsets, and full ten-class trainval are
different protocols. MV attributes are not produced by a learned attribute head.
Excluded cone/barrier TP terms can be NaN without a NaN training loss.

Record the code revision, resolved config, dependency versions, data conversion
provenance, checkpoint origin, and selection criterion:

```powershell
git rev-parse HEAD
python -m pip freeze > environment-resolved.txt
```

## Tests and troubleshooting

Focused tests for the supported workflows, run from the root:

```powershell
python -m pytest tests/test_datasets/test_nuscenes_pkl_camera_order.py -q
python -m pytest tests/test_models/test_mvfcos3d_nuscenes.py -q
python -m pytest tests/test_models/test_task_modules/test_coders/test_fcos3d_bbox_coder.py tests/test_models/test_task_modules/test_coders/test_pgd_bbox_coder.py -q
```

Camera-order tests exercise conversion ordering. MV tests cover registration,
guards, velocity-aware targets/gradients and prediction, with some paths depending
on CUDA. Coder tests cover the mono decoders. These commands do not establish
full-dataset accuracy. The complete `tests/` tree includes upstream tests for
components removed from the trimmed package; a full-suite run can fail for that
reason and is not a substitute for reporting focused results.

| Symptom | First check |
| --- | --- |
| `ModuleNotFoundError` or wrong model registration | Activated environment, editable install, imported package path, MV custom imports |
| MMCV operator load failure | Compatible PyTorch/CUDA/MMCV build with compiled ops |
| Demo fails on `mmdet3d.apis` | Standalone demo API is absent; use the implemented test loop |
| Missing `v1.0-trainval` on Mini | Conversion version and mono metainfo overrides; do not rename folders |
| Image path contains duplicate folders | PKL `img_path`, dataset root, and per-camera `data_prefix` |
| `persistent_workers` error | Set it false when workers are zero |
| Windows multiprocessing fails | Use spawn and zero-worker starter settings |
| Invalid 9D reshape or anchor mismatch | Head, coder, velocity targets, and priors must agree in loss and prediction |
| MV height/kernel assertion | Verify 12 input vertical voxels and neck reductions |
| Resume immediately finishes | Total `max_epochs` must exceed restored epoch |
| Missing best-NDS key | Match evaluator protocol and checkpoint save key; export-only evaluation has no NDS |
| PGD evaluation checkpoint missing | Inspect checkpoint hook and actual output files; configure periodic saves |
| Custom `DumpResults` rejects arguments | Replace evaluator with `_delete_=True` in a child config |
| Low mAP despite decreasing loss | Verify tokens, full GT projections, frame conventions, class order, resize, and split before changing epochs |
| CUDA out of memory | Begin with batch 1; full MV grid is larger than smoke; record any image/grid changes |

See [troubleshooting](troubleshooting.md), [evaluation](evaluation.md), and
[validation evidence](validation.md) for deeper diagnosis and prior evidence.

## Changing the repository

| Intended change | Start here | Verify afterwards |
| --- | --- | --- |
| Dataset location | Child config or nested CLI path overrides | First resolved image/annotation paths and evaluator metadata |
| New raw annotation format | Converter and dataset parser | Schema, class IDs, frame transforms, complete GT projections |
| Image size/augmentation | Dataset pipeline and projection metadata | Intrinsics, centers, boxes, and all six MV views |
| Number/order of classes | Dataset metainfo, head, coder priors/anchors, evaluator | Label mappings and checkpoint compatibility |
| LR, epochs, validation interval | Experiment config optimizer/scheduler/loop | Resolved config and actual logged schedule |
| Mono decoding | Relevant head and box coder | Focused coder/head tests and calibrated predictions |
| MV velocity | 9D head, coder, GT velocity, loss weights | Assignment, nonzero velocity gradients, prediction, formatting, mAVE |
| MV grid dimensions | Projection range, voxel size, voxel neck | Spatial axes, height reductions, forward/loss/predict |
| Export/evaluation protocol | Metric config and `nuscenes_metric.py` | Token coverage, frames, attributes, metric interpretation |

Prefer a dedicated experiment config for reproducibility. Keep each run in a
separate work directory. Preserve upstream attribution and the Apache-2.0 license.
For related guides, return to the [documentation home](index.md).
