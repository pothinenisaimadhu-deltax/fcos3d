# FCOS3D NuScenes data generation and validation

This document is the operational runbook and current validation record for the
camera-only FCOS3D NuScenes-style dataset used by this repository. It covers
data conversion, V2 PKL validation, camera geometry, configuration checks,
checkpoint compatibility, and the remaining manual gates before training.

## Current project status

The KATECH batch-2 dataset was converted on the Saturn machine from:

```text
/hdd2/automotive_perception_group/datasets/kadif/katech_3D/batch_2/nuscenes_katech
```

The generated V2 PKLs are stored in:

```text
/home/shagufta/fcos3d_sai/pkl_file
```

The custom scene split is defined by:

```text
v1.0-trainval/splits.json
```

The converter found 31 scenes and 1,218 samples. The split currently contains:

| Split | Scenes | Samples |
|---|---:|---:|
| Train | 24 | 938 |
| Validation | 7 | 280 |
| Total | 31 | 1,218 |

The earlier 1,000/218 expectation does not describe this `splits.json`.
NuScenes splits are scene-based, so 938/280 is the correct contract unless the
scene assignments are deliberately changed.

The latest completed legacy-validator run passed all enforced checks with the
938/280 expectation. It also reported 218 train and 52 validation velocity
records containing non-finite values. The legacy dataset loader replaces these
values with `[0, 0]`; the strict validator treats them as data that should be
repaired or handled by explicitly disabling velocity prediction.

## Validation target

Validate the pipeline in this order:

```text
raw NuScenes JSON tables
  -> token and foreign-key integrity
  -> scene-based train/validation split
  -> V2 PKL structure
  -> images and per-camera annotations
  -> camera geometry and projections
  -> camera-only resolved configuration
  -> checkpoint/model compatibility
  -> real dataloader batch
  -> visual ground-truth inspection
  -> optional short finite-loss training check
```

The validator intentionally does not run an optimizer or training iteration.

## Repository components

| Path | Purpose |
|---|---|
| `tools/create_data.py` | Generates legacy infos, converts them to V2 PKLs, and invokes validation |
| `tools/dataset_converters/nuscenes_converter.py` | Reads NuScenes tables and creates split infos |
| `tools/dataset_converters/update_infos_to_v2.py` | Converts legacy infos into `metainfo` + `data_list` format |
| `tools/validate_fcos3d_nuscenes.py` | Performs static, configuration, checkpoint, and dataloader checks |
| `configs/_base_/datasets/nus-mono3d.py` | Defines the camera dataset, classes, modality, and pipelines |
| `configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py` | Active FCOS3D model and pipeline configuration |
| `tools/misc/browse_dataset.py` | Renders annotations for mandatory visual inspection |

## Expected dataset layout

```text
nuscenes_katech/
|-- v1.0-trainval/
|   |-- sensor.json
|   |-- calibrated_sensor.json
|   |-- sample.json
|   |-- sample_data.json
|   |-- sample_annotation.json
|   |-- instance.json
|   |-- scene.json
|   |-- ego_pose.json
|   `-- splits.json
|-- samples/
|   |-- CAM_FRONT/
|   |-- CAM_FRONT_LEFT/
|   |-- CAM_FRONT_RIGHT/
|   |-- CAM_BACK/
|   |-- CAM_BACK_LEFT/
|   `-- CAM_BACK_RIGHT/
`-- maps/

pkl_file/
|-- nuscenes_infos_train.pkl
`-- nuscenes_infos_val.pkl
```

LiDAR point files are not model inputs for this camera-only workflow, although
NuScenes-style metadata can still contain LiDAR-related records.

## Generate the PKLs

Run from the repository root on Saturn:

```bash
PYTHONPATH=. python3 tools/create_data.py nuscenes \
  --root-path "/hdd2/automotive_perception_group/datasets/kadif/katech_3D/batch_2/nuscenes_katech" \
  --out-dir "/home/shagufta/fcos3d_sai/pkl_file" \
  --extra-tag nuscenes \
  --version v1.0
```

The converter may overwrite existing PKLs in the output directory. Preserve a
copy first when the existing artifacts are needed for comparison.

Expected split output for the current `splits.json`:

```text
train scene: 24, val scene: 7
train sample: 938, val sample: 280
```

The missing `v1.0-test` message is expected for a train/validation-only custom
dataset and is not a validation failure.

## Run the validator

### Strict validator in this repository

The current validator requires raw metadata, the resolved configuration, and a
checkpoint. It also loads one real training batch. Run:

```bash
PYTHONPATH=. python3 tools/validate_fcos3d_nuscenes.py \
  --data-root "/hdd2/automotive_perception_group/datasets/kadif/katech_3D/batch_2/nuscenes_katech" \
  --ann-root "/home/shagufta/fcos3d_sai/pkl_file" \
  --metadata-root "/hdd2/automotive_perception_group/datasets/kadif/katech_3D/batch_2/nuscenes_katech/v1.0-trainval" \
  --config "configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py" \
  --checkpoint "/home/shagufta/FCOS3D/mmdetection3d/checkpoints/fcos3d_r101_caffe_fpn_gn-head_dcn_2x8_1x_nus-mono3d_finetune_20210717_095645-8d806dc2.pth" \
  --expected-train-samples 938 \
  --expected-val-samples 280 \
  --projection-tolerance 0.1 \
  --max-projection-error 2.0
```

If `--max-projection-error` is rejected, that machine is running the older
validator. Synchronize `tools/validate_fcos3d_nuscenes.py` from this repository
before claiming strict-validator coverage.

Do not split a quoted filesystem path across physical lines. A newline inside
quotes becomes part of the path on Linux. Use a backslash outside the closing
quote for line continuation, as shown above.

### Legacy validator

The older Saturn validator can be run without the maximum-error option:

```bash
PYTHONPATH=. python3 tools/validate_fcos3d_nuscenes.py \
  --data-root "/hdd2/automotive_perception_group/datasets/kadif/katech_3D/batch_2/nuscenes_katech" \
  --ann-root "/home/shagufta/fcos3d_sai/pkl_file" \
  --metadata-root "/hdd2/automotive_perception_group/datasets/kadif/katech_3D/batch_2/nuscenes_katech/v1.0-trainval" \
  --config "configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py" \
  --checkpoint "/home/shagufta/FCOS3D/mmdetection3d/checkpoints/fcos3d_r101_caffe_fpn_gn-head_dcn_2x8_1x_nus-mono3d_finetune_20210717_095645-8d806dc2.pth" \
  --expected-train-samples 938 \
  --expected-val-samples 280 \
  --projection-tolerance 0.1
```

## Checks performed by the strict validator

### Raw metadata

- Required JSON tables exist.
- `calibrated_sensor.sensor_token` resolves to `sensor`.
- `sample_data.calibrated_sensor_token` resolves to `calibrated_sensor`.
- `sample_data.sample_token` resolves to `sample`.
- `sample_data.ego_pose_token` resolves to `ego_pose`.
- Annotation sample and instance tokens resolve correctly.
- Sample scene tokens resolve correctly.
- Duplicate `(sample_token, instance_token)` annotations are rejected.

### V2 PKLs and splits

- Top-level `metainfo` and `data_list` keys exist.
- Expected sample counts match.
- Sample tokens are present and unique within each split.
- Train and validation tokens have zero overlap.
- `metainfo.categories` uses contiguous active IDs; `-1` is allowed only for
  ignored classes.
- Train and validation category mappings agree.
- PKL classes and configured classes agree exactly.
- Annotation labels are integral and are present in the category mapping.

### Images and camera annotations

- Every sample contains exactly the six expected camera names.
- Every sample contains matching `cam_instances` entries for all six cameras.
- Every referenced camera image exists.
- Each camera annotation contains `bbox`, `bbox_3d`, `bbox_label_3d`,
  `center_2d`, and `depth`.
- Duplicate camera instances are rejected.
- 2D boxes are finite and have positive width and height.
- 3D dimensions are finite, positive, and no larger than 30 metres.
- `center_2d` is exactly two finite values.
- Depth is finite, positive, and agrees with camera-space box Z.
- Yaw is finite and lies in `[-pi, pi]`.
- Non-finite velocity values fail strict validation.

### Calibration and projection

- `cam2img` is a finite 3x3 matrix with positive focal lengths.
- `cam2ego` and `lidar2cam` are finite 4x4 matrices.
- Rotation blocks are orthogonal and have determinant approximately `+1`.
- Homogeneous matrix bottom rows equal `[0, 0, 0, 1]`.
- Projected 3D centers agree with `center_2d`.
- Mean projection error is below 0.1 px by default.
- Maximum projection error is at most 2 px by default.

### Resolved configuration

- Model type is `FCOSMono3D`.
- Head is `FCOSMono3DHead` or `PGDHead`.
- All splits use `use_camera=True` and `use_lidar=False`.
- `load_type='mv_image_based'`.
- `box_type_3d='Camera'`.
- Pipelines include `LoadImageFromFileMono3D` and `Pack3DDetInputs`.
- The training pipeline includes `LoadAnnotations3D`.
- Pipelines do not include `LoadPointsFromFile` or `ObjectSample`.

### Checkpoint and dataloader

- The configured model is constructed.
- Checkpoint tensor names and shapes are loaded into the model.
- Missing, unexpected, or shape-mismatched keys fail validation.
- A real training dataloader is built with one worker-free batch.
- The batch contains `inputs` and `data_samples`.

The dataloader check is not a training iteration: it does not run a forward
pass, calculate losses, backpropagate, or update model weights.

## Recorded validation results

The completed legacy-validator run reported:

| Check | Train | Validation | Result |
|---|---:|---:|---|
| Samples | 938 | 280 | Pass for current split |
| Camera annotations | 15,450 | 5,010 | Loaded |
| Duplicate camera instances | 0 | 0 | Pass |
| Mean projection error | 0.000059 px | 0.000061 px | Pass |
| Maximum projection error | 0.018594 px | 0.019165 px | Pass |
| Projection errors above 2 px | 0 | 0 | Pass |
| Non-finite velocity records | 218 | 52 | Warning in legacy validator |

Additional results:

- All checked JSON foreign-key failure counts were zero.
- Duplicate raw sample/instance annotations were zero.
- Train/validation token overlap was zero.
- The checkpoint contained 777 keys.

The class-label counts contained IDs 0, 1, 3, 4, 5, 6, and 7. IDs 2, 8,
and 9 had no annotations in these PKLs. This is not automatically corruption,
but it should be confirmed against the intended class distribution before
training and evaluation.

## Velocity decision

The active FCOS3D head predicts velocity. Choose and document one policy:

1. Repair the 270 non-finite velocity records using valid targets in the
   correct coordinate frame and units; or
2. Deliberately disable velocity prediction and remove its target requirement
   from the model/dataset configuration.

Do not silently treat unknown motion as stationary without accepting the label
noise this introduces. The legacy loader's `[0, 0]` replacement is a fallback,
not proof that the targets are correct.

## Mandatory visual inspection

Numerical projection checks do not prove that box dimensions, class identity,
or orientation are visually correct. Render 20-50 representative samples,
covering all six cameras, different scenes, near/far objects, truncation, and
occlusion:

```bash
PYTHONPATH=. python3 tools/misc/browse_dataset.py \
  configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py \
  --task mono_det \
  --output-dir work_dirs/gt_verify
```

Inspect the output for:

- boxes landing on the corresponding objects;
- correct class labels;
- plausible width, length, height, depth, and orientation;
- correct behavior at image boundaries;
- consistent results across all camera views.

Visual approval cannot be inferred from the validator's pass message.

## Go/no-go checklist

| Gate | Required result | Current evidence |
|---|---|---|
| Raw JSON relationships | Zero broken relationships | Pass |
| Duplicate raw annotations | Zero | Pass |
| V2 PKL structure | `metainfo` + `data_list` | Pass |
| Split sizes | 938 train / 280 val | Pass |
| Split overlap | Zero shared sample tokens | Pass |
| Six cameras | Present in every sample | Legacy run passed enforced structure |
| Image existence | Every referenced file exists | Legacy run passed enforced structure |
| Duplicate camera instances | Zero | Pass |
| Positive depth and depth/Z agreement | Zero failures | Legacy run passed |
| Intrinsics and extrinsics | Valid matrices | Legacy run passed |
| Projection mean | Below 0.1 px | Pass |
| Projection maximum | At most 2 px | Observed pass; strict enforcement pending on Saturn |
| 2D/3D boxes and yaw | Finite and physically valid | Legacy run passed |
| Category/config alignment | Exact | Strict-validator run pending on Saturn |
| Velocity | Valid targets or head disabled | Decision required |
| Camera-only configuration | Correct modality and pipeline | Legacy config check passed; strict checks pending |
| Exact checkpoint load | No missing/unexpected/mismatched keys | Strict-validator run pending on Saturn |
| One dataloader batch | Loads `inputs` and `data_samples` | Strict-validator run pending on Saturn |
| Visual GT inspection | Human-approved render set | Pending |
| Finite training losses | Optional short training check | Intentionally not included |

Training is a no-go until the velocity policy is explicit and visual inspection
is approved. For the strongest automated gate, synchronize and run the strict
validator on Saturn as well.

## Troubleshooting

### `unrecognized arguments: --max-projection-error`

The machine has the legacy validator. Update
`tools/validate_fcos3d_nuscenes.py` from this repository or omit the option and
treat the result as legacy coverage only.

### Raw metadata files appear missing

Check that the quoted path contains no embedded newline:

```bash
printf '<%s>\n' "/path/to/nuscenes_katech/v1.0-trainval"
ls -l "/path/to/nuscenes_katech/v1.0-trainval/sensor.json"
```

### PKLs appear missing

`--ann-root` must be the directory containing the PKLs, not necessarily the
repository's `samplers` directory:

```bash
find /home/shagufta/fcos3d_sai /hdd2 -type f \
  \( -name 'nuscenes_infos_train.pkl' -o -name 'nuscenes_infos_val.pkl' \) \
  2>/dev/null
```

### Expected sample counts fail

Inspect `v1.0-trainval/splits.json` and the converter's scene/sample summary.
Do not change expected counts merely to silence a failure. First confirm that
the scene allocation is intentional and leakage-safe.

### Velocity warnings appear

Locate the non-finite source velocities and determine whether they represent
unknown motion, missing pose history, or a conversion error. Repair them or
disable the velocity branch explicitly.

## Final validation evidence to retain

For a reproducible training handoff, archive:

- the exact `splits.json`;
- train and validation PKL hashes;
- the resolved config;
- checkpoint path and hash;
- strict validator console output;
- rendered GT inspection samples and reviewer approval;
- the documented velocity policy;
- the repository commit used for conversion and validation.

