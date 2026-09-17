# FCOS3D dataset workflows

## nuScenes

Use `python -m tools.create_data nuscenes --root-path DATA --out-dir DATA`.
Train or test with a config in `configs/fcos3d/` or `configs/pgd/`.

Data creation automatically runs the strict FCOS3D validator after converting
the train and validation PKLs. A validation failure leaves the generated files
in place for diagnosis but exits with an error so training is not started with
known-invalid annotations. Use `--skip-validation` only while debugging the
converter.

The validator can also be run independently:

```powershell
python tools/validate_fcos3d_nuscenes.py `
  --data-root "C:\path\to\nuscenes" `
  --ann-root "C:\path\to\pkl-output" `
  --metadata-root "C:\path\to\nuscenes\v1.0-trainval" `
  --config configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py `
  --checkpoint checkpoints/fcos3d_checkpoint.pth
```

Use `--expected-train-samples` and `--expected-val-samples` when exact split
sizes are part of the dataset contract. Visual alignment and finite-loss checks
still require rendered sample inspection and a short training run.

## Custom camera data

Write `custom_train.json` and `custom_val.json` using the NuScenes v2 JSON
records accepted by `NuScenesJsonDataset`. Validate each manifest before use:

```powershell
python tools/validate_custom_nuscenes_json.py data/custom/custom_train.json
python tools/train.py configs/custom/fcos3d_custom_nuscenes_json.py
python tools/test.py configs/custom/fcos3d_custom_nuscenes_json.py CHECKPOINT
```

Use `configs/custom/pgd_custom_nuscenes_json.py` for PGD (FCOS3D++).
