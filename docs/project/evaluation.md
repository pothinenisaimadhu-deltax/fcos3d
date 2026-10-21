# Evaluation and visualization

## Evaluate a compatible checkpoint

Use the config matching the trained model, class order and preprocessing.
Override the **test** dataloader and evaluator, not only the validation paths.

PowerShell example:

```powershell
$datasetRoot = (Resolve-Path "data/nuscenes").Path
$annotationRoot = (Resolve-Path "data/nuscenes_infos").Path
python tools/test.py configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py work_dirs/mvfcos3d_mini/epoch_30.pth --work-dir work_dirs/mvfcos3d_mini_eval --cfg-options "test_dataloader.dataset.data_root=$datasetRoot" "test_dataloader.dataset.ann_file=$annotationRoot/nuscenes_infos_val.pkl" "test_evaluator.data_root=$datasetRoot" "test_evaluator.ann_file=$annotationRoot/nuscenes_infos_val.pkl"
```

For mono Mini evaluation also override
`test_dataloader.dataset.metainfo.version=v1.0-mini`. Windows mono requires
spawn and appropriate worker settings as described in [training](training.md).
`epoch_30.pth` is an example: select an existing compatible checkpoint.

For a persistent NuScenes-format prediction JSON, provide
`test_evaluator.jsonfile_prefix=work_dirs/RUN/predictions`. Otherwise the
metric can use temporary output. Do not confuse raw prediction export with
scored evaluation. A custom JSON config using DumpResults exports predictions,
not official NuScenes mAP/NDS.

## Version and split correctness

| Mode | Metadata | Evaluation protocol |
| --- | --- | --- |
| Official Mini | v1.0-mini | mini_val tokens |
| Official trainval | v1.0-trainval | official val tokens |
| Explicit custom subset | matching JSON tables | exactly the annotation PKL tokens |

The MV adapter uses PKL metainfo.version. The inherited mono dataset default
can be trainval unless explicitly overridden. The evaluator must load JSON
metadata containing every predicted sample token.

`eval_subset=True` is a custom protocol. It loads GT for exactly the PKL
tokens and requires the prediction token set to match. Use it intentionally
for custom subsets, not to relabel a partial experiment as an official benchmark.
The subset smoke helper creates a temporary one-sample annotation file, leaving
the source PKL untouched.

## Metrics are not ordinary classification accuracy

NuScenes reports distance-threshold AP and true-positive errors. Consult the
[official detection specification](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md)
for full definitions.

| Log field | Interpretation | Preferred direction |
| --- | --- | --- |
| mAP | Detection quality averaged over classes and matching thresholds | Higher |
| NDS | Composite detection score combining AP and TP-quality terms | Higher |
| ATE / mATE | Translation error, meters | Lower |
| ASE / mASE | Scale error | Lower |
| AOE / mAOE | Orientation error, radians | Lower |
| AVE / mAVE | Velocity error, meters/second | Lower |
| AAE / mAAE | Attribute error | Lower |

AP_dist_0.5/1.0/2.0/4.0 uses center-distance matching, not image IoU accuracy.
Vehicles can look plausible in 2D while failing strict 3D localization.
Do not describe NDS=0.389 as 38.9% ordinary classification accuracy.

Some undefined TP terms show NaN by design: cones do not have the same
orientation/velocity/attribute evaluation as moving vehicles, and barriers
exclude some motion-related terms. These are different from a NaN training
loss. Some no-qualifying-match TP errors default to 1; they are not proof
that every prediction has exactly that numerical error.

## Car-only and multi-class evaluation

This fork can publish CustomCarOnly metric keys for an explicitly car-only
class configuration. Its AP/NDS protocol differs from ten-class evaluation.
Do not compare a car-only result with ten-class mAP as a fair model improvement.
Likewise Mini/custom-scene/official val results are different datasets.

MV has no learned attribute branch. The LiDAR-box formatter derives/defaults
attributes using class and velocity rules. AAE from that path must not be
presented as evidence of an attribute classifier.

## Visual inspection and six-camera video

Use rendered predictions together with GT for checking yaw, dimensions and
alignment. The repository retains visualization tooling, but upstream examples
for removed LiDAR models are not supported workflow instructions.
The generic visualizer's six-view rendering should be verified for the chosen
output format before relying on a publication video.

For existing per-camera rendered images:

```bash
python tools/stitch_nuscenes_cameras.py --input-root work_dirs/RUN/view_results --ann-file data/nuscenes_infos/nuscenes_infos_val.pkl --output-dir work_dirs/RUN/camera_mosaic --image-kind 3d --fps 10 --width 640 --height 360
```

Preferred grouping is by the annotation PKL, which specifies each sample's
camera filenames. Missing matching renders cause groups to be skipped.
Without PKL grouping, positional sequence matching can misalign views when
files are missing; the fallback is not a guarantee of timestamp synchronization.

`--clean-output` removes previously generated frames/video from the output
directory. Use a dedicated generated-output directory. Do not promise
“no missing frames” unless counts and identities have been checked.
Tile labels can cover part of the rendered image, and resizing changes display
resolution: videos are qualitative artifacts, not evaluation evidence.

## What to publish

Publish the evaluated split, class protocol, checkpoint, resolved config,
dataset conversion provenance, metric version and selection criterion.
Share representative success and failure cases, not only selected detections.
Review images, JSON tokens and logs for customer/employee information before
release.
