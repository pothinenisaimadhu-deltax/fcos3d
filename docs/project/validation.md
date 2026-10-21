# Validation evidence and result reporting

## Verified implementation checks

During local integration the following focused checks completed:

| Check | Evidence | What it does not prove |
| --- | --- | --- |
| MV configuration and entrypoint guards | Regression test passed | Full training quality |
| PKL version and deterministic camera order | Regression test passed | Every real calibration is correct |
| 9D assignment and velocity gradients | Nonzero velocity-coordinate gradients | Useful real-world motion accuracy |
| 9D prediction decoding | CUDA predictions with nine coordinates | Good AP/NDS |
| Reduced-grid R101/DCNv2 loss/backward/predict | CUDA regression test passed | Full-grid memory or convergence |
| Real local NuScenes Mini smoke | Finite loss, prediction and subset evaluation completed | An epoch, optimizer updates or trained-model accuracy |
| Camera-order PKL conversion | Two converter regression tests passed | Validation of all original records |
| Mono coder regressions | Existing FCOS3D/PGD coder tests passed | Exhaustive regression coverage |

The initial MV test suite had four passing tests; the separate converter suite
had two, and existing mono coder checks had two. This is a point-in-time record,
not a claimed CI badge or a maintained benchmark. Rerun on your release commit.

## Reproduce focused tests

```bash
python -m pytest tests/test_models/test_mvfcos3d_nuscenes.py tests/test_datasets/test_nuscenes_pkl_camera_order.py tests/test_models/test_task_modules/test_coders/test_fcos3d_bbox_coder.py tests/test_models/test_task_modules/test_coders/test_pgd_bbox_coder.py -q
```

Some MV tests require CUDA and skip that portion without it. Inspect skipped
tests; a CPU-only green result is not a GPU operator validation.
Afterward run the real-data smoke command from the training guide.

## Before a long run

1. Verify environment versions, module path and compiled operators.
2. Validate dataset/version/class mapping and train/val scene separation.
3. Verify every image path and complete six-camera records.
4. Render ten diverse samples with GT corners, yaw and dimensions.
5. Check finite velocity targets and distributions by class.
6. Exercise forward/backward/predict/evaluation on actual data.
7. Attempt a small no-augmentation overfit experiment if geometry is uncertain.
8. Review resolved config, optimizer groups and scheduler boundaries.
9. Train a full run and monitor validation, not only training loss.

Failure to overfit can indicate geometry, target assignment, capacity or
optimization problems; it does not uniquely prove an annotation bug.
A successful overfit check likewise does not prove generalization.

## Results publication template

| Field | Required record |
| --- | --- |
| Model/config | Exact config and resolved overrides |
| Commit | Source revision plus local diff if applicable |
| Environment | Python/PyTorch/CUDA/MMCV/MMEngine/MMDetection/devkit versions |
| Data | Version, scenes/split, samples, conversion revision and data hash |
| Protocol | Official ten-class, explicit car-only or custom subset |
| Initialization | Checkpoint URL/source/hash or random/backbone initialization |
| Training | Optimizer, all LR groups, schedule, batches, devices, epochs |
| Selection | Best NDS, best mAP or last epoch |
| Evaluation | Checkpoint hash, evaluator settings and exported summary |
| Performance | AP/NDS/errors, throughput, peak memory and conditions |
| Limitations | Missing classes, failure examples, uncertainty and scope |

Use one row per experiment. Distinguish best-epoch and final-epoch metrics.
Do not take the highest mAP and highest NDS from different checkpoints and
present them as one checkpoint's scores.

## Historical experiments

The conversation and archived logs contain runs with different datasets,
class protocols, fine-tuning choices and evaluation settings. They are not
a single comparable benchmark. This documentation deliberately does not
publish those numbers as a company performance claim without checked artifacts.

NuScenes Mini is useful for execution and small-data research; it is not
substitute evidence for performance on the full benchmark or customer scenes.
The random-weight smoke metrics are intentionally not reported as achievements.

## Roadmap, not completed features

- Validate full-grid convergence and GPU memory on a supported platform matrix.
- Provide reviewed reproducible environment pins.
- Audit remaining mono pipeline geometry, especially inherited PGD resizing.
- Expand evaluator tests and full-split validation evidence.
- Add separate velocity diagnostics without changing loss accounting.
- Explore temporal input only with an explicit temporal data/transform design.
- Establish deployment/latency/privacy/safety validation before product use.

These are future validation or engineering tasks, not features already shipped.
