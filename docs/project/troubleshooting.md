# Troubleshooting and learning quality

## Separate execution from accuracy

A completed epoch establishes execution, not correct geometry or convergence.
Low mAP across FCOS3D, PGD and MV-FCOS3D is a reason to inspect shared data and
evaluation first. It does not prove a particular conversion error. A decreasing
training loss can coexist with incorrect coordinates, overfitting or poor
generalization. Do not extend a 100-epoch run without examining evidence.

## Common execution failures

| Symptom | Check and scoped correction |
| --- | --- |
| Metadata folder v1.0-trainval missing | For official Mini use `--version v1.0-mini`; do not rename its JSON directory to trainval. |
| Image FileNotFoundError | Inspect the actual resolved PKL img_path and data_prefix. A basename may need samples/CAM_FRONT/...; do not prepend the root twice. |
| NuScenesMultiViewDataset not registered | Use the MV config's custom imports and verify Python imports this checkout. Copying a config alone does not install its adapter. |
| Entry point rejects MultiViewDfM | Confirm this checkout has the MV-aware entry points. Do not remove all validation from a mono-only copy. |
| Invalid reshape to 9D in prediction | Check 9D coder, head and velocity-extended priors in both training and prediction. Updating only get_anchors is insufficient. |
| Anchor/GT dimension assertion | Both must match: 9D includes vx/vy; 7D does not train velocity. |
| 3D kernel too large or final height assertion | Inspect vertical voxel count and neck reductions. The current MV recipe starts with 12 vertical voxels; setting height to one at input is not a fix. |
| Resume exits without another epoch | max_epochs is the total target. Resuming epoch 10 with max_epochs=10 has no remaining epochs. |
| Resume GPU-count warning | Verify checkpoint origin, world size and batch/LR policy. Do not resume a public mono checkpoint as an MV continuation. |
| cfg-options parsing failure | Each argument must be one key=value token, e.g. train_cfg.max_epochs=10, without a space after equals. |
| Shell reports File/traceback as commands | Paste only the command, not logs/prompts. Bash backslashes must end the line; PowerShell uses different continuation syntax. |

ImageNet ResNet weights may contain unused fc keys and omit DCN offset weights.
Those warnings are not the same as failure to load a complete detector checkpoint.
Inspect intended initialization and matching layers; mono PGD/FCOS heads are not
drop-in pretrained MV anchor heads. Deprecation warnings also do not establish
the cause of low AP. A training loss becoming NaN/Inf is different and requires
stopping to inspect targets, operators and gradients.

## Vehicles detected but heading or position is wrong

Inspect ground truth before changing the detector:

1. Select ten samples across scenes and cameras, including near/far objects.
2. Verify image path, token and timestamp association.
3. Project full GT box corners, not only centers, using the same conventions as
   the model. Check positive depth, dimensions, yaw and box origin.
4. Compare camera-frame mono GT with common-frame MV GT for the same object.
5. Check class ordering against PKL metainfo and checkpoint class ordering.
6. Confirm each image has its matching intrinsic/extrinsic matrices after any
   reordering. Inspect resized/cropped projection in the actual pipeline.
7. Check conversion back to global coordinates in the evaluator against raw JSON.

For column-vector transforms at a common pose, lidar2cam is inverse(cam2ego)
times lidar2ego. Asynchronous camera/ego poses may need additional pose
composition. A successful center reprojection alone does not validate yaw or
length/width conventions. Do not relabel ego2cam as lidar2cam for LiDAR-frame GT.
See [data preparation](data-preparation.md).

Use a small overfit experiment with augmentation disabled, then examine both
training-set predictions and GT. Failure to fit those samples may indicate data,
assignment, optimization or architecture issues; it is not proof of one cause.
Only then compare a fresh full run with controlled LR and checkpoint selection.

## Velocity plateau

The MV head has three reported losses: loss_cls, loss_bbox and loss_dir.
Its 9D loss_bbox includes velocity. Mono FCOS3D/PGD can expose loss_velo
separately. Missing a separate log field does not prove velocity is disabled.
Conversely, an evaluation AVE alone does not prove velocity was trained.

Audit finite velocity counts, zero ratios **per class**, speed percentiles,
track associations, time units and coordinate rotation. Stationary objects
legitimately have zero velocity; one zero-valued sample is not evidence of
collapsed labels. Missing targets replaced with zero are not genuine stationary
measurements. Inspect the converter and raw tracks before repairing targets.

Single-time six-camera input provides spatial evidence, not measured temporal
motion. It can still learn velocity cues statistically, but temporal input is
an architectural/data extension, not just changing num_ref_frames. Track mAVE
alongside class-specific errors and geometry. Do not claim that reducing
aggregate bbox loss necessarily improves velocity.

## Evaluation looks suspicious

Check Mini/trainval version, JSON root, split, sample-token coverage, class names
and output frame. Subset evaluation must intentionally use the annotation PKL's
token set. The training and validation scene sets should not overlap.
Cone/barrier NaNs for excluded metrics are expected; they are not NaN losses.
Errors of 1 can be fallback values for insufficient qualifying matches.
Read [evaluation](evaluation.md) before comparing results.

## Reporting a reproducible issue

Provide commit, model/config, sanitized command, dependency/CUDA versions,
checkpoint origin, resolved paths without private names, smallest relevant
traceback and a permitted minimal example. Include whether focused tests and
the small smoke check pass. Do not upload confidential camera footage, full
datasets, arbitrary pickle files or credentials to public issues.
