# Installation and environment verification

## Compatibility

Use an isolated environment. The import guards in `mmdet3d/__init__.py` require:

| Package | Range |
| --- | --- |
| MMCV | >=2.0.0rc4,<2.2.0 |
| MMEngine | >=0.8.0,<1.0.0 |
| MMDetection | >=3.0.0rc5,<3.4.0 |

These ranges are not a full tested matrix. The local Windows verification
environment used Python 3.10, PyTorch 2.0.0+cu118 and MMCV 2.1.0 with CUDA.
That establishes only the checks reported in [validation](validation.md).

R101 recipes use deformable convolution and rotated NMS. Install MMCV with
compiled operators, not only mmcv-lite. Match its binary/build to PyTorch and
CUDA. [Upstream setup](https://mmdetection3d.readthedocs.io/en/latest/get_started.html)
provides platform-specific background; this fork's version guards still apply.

## Installation outline

Install a compatible CUDA-enabled PyTorch build first, then from this checkout:

```bash
python -m pip install -U openmim
mim install "mmengine>=0.8.0,<1.0.0"
mim install "mmcv>=2.0.0rc4,<2.2.0"
mim install "mmdet>=3.0.0rc5,<3.4.0"
python -m pip install -v -e .
python -m pip install pytest
```

This is not a lockfile or a universal reproducible install. If no matching
MMCV wheel exists, follow its source-build instructions rather than mixing
unrelated binaries. Runtime dependencies are listed in
`requirements/runtime.txt`. Review resolver output before updating an existing
environment.

The package retains the name `mmdet3d`; another editable fork can shadow it.
Training/test scripts prioritize this checkout, but verify interactive imports.

## Preliminary checks

```bash
python -c "import torch, mmcv, mmengine, mmdet, mmdet3d; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(mmcv.__version__, mmengine.__version__, mmdet.__version__); print(mmdet3d.__file__)"
python -c "from mmcv.ops import ModulatedDeformConv2dPack, nms_rotated; print('Compiled operators imported')"
python -m pip check
```

Operator imports are preliminary checks. The MV smoke command actually runs
CUDA. Inspect `nvidia-smi` while running for GPU process and memory evidence.

## Windows and Linux

Windows uses PowerShell backticks for continuation and `spawn` multiprocessing.
If `num_workers=0`, also set `persistent_workers=False`. The MV config uses
spawn; some mono configs inherit fork and require an override on Windows.

Linux Bash uses a trailing backslash. `CUDA_VISIBLE_DEVICES=2` exposes physical
GPU 2 as logical GPU 0 inside the process. Run from the repository root.

Do not add a space after an override's equals sign or continuation character.
Do not paste prompts/log prefixes into commands.

## Reproducibility

```bash
python -m pip freeze > environment-resolved.txt
git rev-parse HEAD
```

Review environment exports for local paths before sharing. Dependency upgrades
require focused tests and a new real-data smoke check. A company release should
supply a reviewed lock/environment file for each supported platform; none is
claimed as universally validated here.
