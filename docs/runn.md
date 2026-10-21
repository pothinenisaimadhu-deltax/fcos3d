# Running the supported workflows

The current DeltaX India guides replace the historical machine-specific command
notes on this page. Run commands from the repository root in your activated
compatible environment. Do not copy shell prompts or traceback text.

- [Installation and GPU checks](project/installation.md)
- [NuScenes Mini/trainval preparation](project/data-preparation.md)
- [Training, batch size, learning rate and resume](project/training.md)
- [Evaluation, export and camera mosaics](project/evaluation.md)
- [Troubleshooting geometry and velocity](project/troubleshooting.md)

For Mini preparation:

```bash
python -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/nuscenes_infos --extra-tag nuscenes --version v1.0-mini
```

Use the full training guide for absolute annotation-path overrides and
platform-specific syntax. Camera-only MV training needs six calibrated views
and common-frame annotations; six arbitrary images are not a valid dataset.
