# DeltaX India Camera-Based 3D Detection

A focused research and engineering repository for **FCOS3D, PGD and NuScenes
MV-FCOS3D**, maintained for DeltaX India. It adapts OpenMMLab MMDetection3D:
the original algorithms and framework are not claimed as company inventions.

Repository: [pothinenisaimadhu-deltax/fcos3d](https://github.com/pothinenisaimadhu-deltax/fcos3d)
| [Documentation](docs/project/index.md)
| [Issues](https://github.com/pothinenisaimadhu-deltax/fcos3d/issues)
| [License](LICENSE)

**Status:** research workflows, not a production perception system. The MV
path has passed reduced-memory CUDA execution checks. Full-resolution
convergence, deployment performance and safety validation are not established
by those checks.

## Supported scope

| Workflow | Input per model sample | Implementation | Supervision / output |
| --- | --- | --- | --- |
| FCOS3D | One image | FCOSMono3D / FCOSMono3DHead | Camera-frame boxes, classes, direction, velocity and configured attributes |
| PGD, called FCOS3D++ in this fork | One image | FCOSMono3D / PGDHead | Monocular depth-related extensions and configured box outputs |
| NuScenes MV-FCOS3D | Six cameras at one timestamp | MultiViewDfM / NuScenesVelocityAnchor3DHead | Common LiDAR-frame 9D boxes, classes and direction |
| Custom JSON mono workflows | One image | FCOS3D or PGD / NuScenesJsonDataset | Prediction export; not automatically official nuScenes scoring |

Camera-only means no LiDAR points are supplied to these detectors. Calibration,
ground-truth boxes and evaluation metadata are still required. `lidar2cam`
is a transformation matrix, not point-cloud input. This trimmed fork does
**not** promise the full upstream model/dataset catalog.

## Improvements in this fork

- NuScenes v2 PKL preparation with frame-level and per-camera annotations.
- Canonical six-camera ordering in conversion and the MV dataset adapter.
- Dataset/projection validation and explicit custom-scene subset evaluation.
- Opt-in registration of multi-view model dependencies.
- A separate 9D anchor head, with velocity priors for training and decoding.
- PKL-driven Mini/trainval version selection in the MV adapter.
- Supported-workflow checks at training and evaluation entry points.
- Focused CUDA, camera-order and velocity-gradient regression tests.

These are integration and reliability improvements, **not demonstrated
AP/NDS improvements**. See [validation and reporting](docs/project/validation.md).

## Documentation

| Guide | Purpose |
| --- | --- |
| [Documentation home](docs/project/index.md) | Reading order and support boundaries |
| [Repository handbook](docs/project/repository-handbook.md) | Detailed file structure, models, configuration, and sample commands |
| [File inventory](docs/project/file-inventory.md) | Complete indexed file list and file responsibilities |
| [Installation](docs/project/installation.md) | Environments, CUDA operators and import checks |
| [Data preparation](docs/project/data-preparation.md) | Mini/trainval, PKL schema, ordering and coordinates |
| [Training](docs/project/training.md) | Commands, batches, LR, fine-tuning and resume |
| [Evaluation](docs/project/evaluation.md) | Splits, metrics, prediction export and mosaics |
| [Architecture](docs/project/architecture.md) | Entry points, modules and losses |
| [Validation](docs/project/validation.md) | Evidence and fair experiment reporting |
| [Troubleshooting](docs/project/troubleshooting.md) | Failures, geometry and velocity debugging |
| [Publication checklist](docs/project/publication.md) | Company release, provenance, privacy and licensing |
| [Contributing](CONTRIBUTING.md) | Review and testing expectations |

Material under `docs/en/` includes retained upstream guidance. Broad examples
may refer to removed models. Use the project guides for supported commands.
Older diagrams and office documents are historical artifacts, not the current
authoritative workflow.

## Quick start

Run from the repository root in a compatible CUDA environment:

```bash
python -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/nuscenes_infos --extra-tag nuscenes --version v1.0-mini
python tools/check_mvfcos3d.py --data-root data/nuscenes --train-ann "$(pwd)/data/nuscenes_infos/nuscenes_infos_train.pkl" --val-ann "$(pwd)/data/nuscenes_infos/nuscenes_infos_val.pkl" --small
```

The second command checks one training/backward pass, prediction and subset
evaluation without saving a checkpoint. It reduces image/grid size for
verification; its metrics do not measure trained-model accuracy.

Use the [complete training command](docs/project/training.md) for a full run.
Some inherited mono configs contain machine-specific defaults; override all
dataset and evaluator paths. Start MV training with batch size 1.

## Reproducibility and responsible use

Record the commit, resolved config, dependencies, dataset version/split,
checkpoint origin and checkpoint selection rule. Car-only, custom-subset and
official ten-class scores are not directly interchangeable. Lower training
loss alone does not prove better detection.

Do not deploy this repository directly in a safety-critical vehicle system.
Independent validation, uncertainty analysis and operational testing remain
required. General questions and reproducible bugs belong in
[this fork's issues](https://github.com/pothinenisaimadhu-deltax/fcos3d/issues),
not upstream's issue tracker unless an upstream defect is confirmed.

## Attribution and license

This fork derives from [MMDetection3D](https://github.com/open-mmlab/mmdetection3d).
Original copyright headers and the [Apache-2.0 license](LICENSE) are retained.
It is not an official OpenMMLab release and does not imply upstream endorsement.

See the [upstream installation guide](https://mmdetection3d.readthedocs.io/en/latest/get_started.html)
for framework setup and the
[nuScenes detection specification](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md)
for benchmark definitions. Dataset, checkpoint and third-party asset terms are
separate from the source-code license. Keep [the upstream citation](CITATION.cff)
when using the inherited framework.
