# Repository file inventory

Snapshot generated on 2026-10-21 from the Git index plus the new handbook files.

This index includes staged files already present in the workspace. It excludes
Git internals, ignored caches, local checkpoints, datasets, and generated runs.
Rows describe file roles, not a guarantee that each inherited component is
supported or runtime-tested. Python symbol names are extracted statically.

See the [repository handbook](repository-handbook.md) for architecture and commands.

## Root files

| File | Role or main definitions |
| --- | --- |
| [.gitignore](../../.gitignore) | Repository configuration or supporting asset: .gitignore. |
| [.pre-commit-config-zh-cn.yaml](../../.pre-commit-config-zh-cn.yaml) | Repository configuration or supporting asset: .pre-commit-config-zh-cn.yaml. |
| [.pre-commit-config.yaml](../../.pre-commit-config.yaml) | Repository configuration or supporting asset: .pre-commit-config.yaml. |
| [.readthedocs.yml](../../.readthedocs.yml) | Repository configuration or supporting asset: .readthedocs.yml. |
| [CITATION.cff](../../CITATION.cff) | Machine-readable upstream citation metadata. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Documentation: Contributing to the DeltaX India fork |
| [LICENSE](../../LICENSE) | Apache-2.0 license and conditions. |
| [MANIFEST.in](../../MANIFEST.in) | Repository configuration or supporting asset: MANIFEST.in. |
| [README.md](../../README.md) | Documentation: DeltaX India Camera-Based 3D Detection |
| [dataset-index.yml](../../dataset-index.yml) | Dataset/model metadata index. |
| [model-index.yml](../../model-index.yml) | Dataset/model metadata index. |
| [requirements.txt](../../requirements.txt) | Dependency declarations for requirements. |
| [setup.cfg](../../setup.cfg) | Repository configuration or supporting asset: setup.cfg. |
| [setup.py](../../setup.py) | Defines readme, get_version, make_cuda_ext, parse_requirements, add_mim_extention. |

## .circleci

| File | Role or main definitions |
| --- | --- |
| [.circleci/config.yml](../../.circleci/config.yml) | CI automation, repository template, or contribution metadata. |
| [.circleci/docker/Dockerfile](../../.circleci/docker/Dockerfile) | CI automation, repository template, or contribution metadata. |
| [.circleci/test.yml](../../.circleci/test.yml) | CI automation, repository template, or contribution metadata. |

## .dev_scripts

| File | Role or main definitions |
| --- | --- |
| [.dev_scripts/benchmark_full_models.txt](../../.dev_scripts/benchmark_full_models.txt) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/benchmark_options.py](../../.dev_scripts/benchmark_options.py) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/benchmark_train_models.txt](../../.dev_scripts/benchmark_train_models.txt) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/covignore.cfg](../../.dev_scripts/covignore.cfg) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/diff_coverage_test.sh](../../.dev_scripts/diff_coverage_test.sh) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/gather_models.py](../../.dev_scripts/gather_models.py) | Script to gather benchmarked models and prepare them for upload. |
| [.dev_scripts/gen_benchmark_script.py](../../.dev_scripts/gen_benchmark_script.py) | Defines parse_args. |
| [.dev_scripts/linter.sh](../../.dev_scripts/linter.sh) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/test_benchmark.sh](../../.dev_scripts/test_benchmark.sh) | Repository maintenance helper; inspect arguments before use. |
| [.dev_scripts/train_benchmark.sh](../../.dev_scripts/train_benchmark.sh) | Repository maintenance helper; inspect arguments before use. |

## .github

| File | Role or main definitions |
| --- | --- |
| [.github/CODE_OF_CONDUCT.md](../../.github/CODE_OF_CONDUCT.md) | Documentation: Contributor Covenant Code of Conduct |
| [.github/CONTRIBUTING.md](../../.github/CONTRIBUTING.md) | Redirects contributors to the root contribution guide. |
| [.github/ISSUE_TEMPLATE/1-bug-report.yml](../../.github/ISSUE_TEMPLATE/1-bug-report.yml) | CI automation, repository template, or contribution metadata. |
| [.github/ISSUE_TEMPLATE/2-feature_request.yml](../../.github/ISSUE_TEMPLATE/2-feature_request.yml) | CI automation, repository template, or contribution metadata. |
| [.github/ISSUE_TEMPLATE/3-new-model.yml](../../.github/ISSUE_TEMPLATE/3-new-model.yml) | CI automation, repository template, or contribution metadata. |
| [.github/ISSUE_TEMPLATE/4-documentation.yml](../../.github/ISSUE_TEMPLATE/4-documentation.yml) | CI automation, repository template, or contribution metadata. |
| [.github/ISSUE_TEMPLATE/config.yml](../../.github/ISSUE_TEMPLATE/config.yml) | CI automation, repository template, or contribution metadata. |
| [.github/pull_request_template.md](../../.github/pull_request_template.md) | Documentation: Thanks for your contribution and we appreciate it a lot. The following instructions would make your pull request more healthy and more easily get feedback. If y |
| [.github/workflows/deploy.yml](../../.github/workflows/deploy.yml) | CI automation, repository template, or contribution metadata. |
| [.github/workflows/lint.yml](../../.github/workflows/lint.yml) | CI automation, repository template, or contribution metadata. |
| [.github/workflows/merge_stage_test.yml](../../.github/workflows/merge_stage_test.yml) | CI automation, repository template, or contribution metadata. |
| [.github/workflows/pr_stage_test.yml](../../.github/workflows/pr_stage_test.yml) | CI automation, repository template, or contribution metadata. |
| [.github/workflows/test_mim.yml](../../.github/workflows/test_mim.yml) | CI automation, repository template, or contribution metadata. |

## configs

| File | Role or main definitions |
| --- | --- |
| [configs/_base_/datasets/nus-mono3d.py](../../configs/_base_/datasets/nus-mono3d.py) | Repository configuration or supporting asset: nus-mono3d.py. |
| [configs/_base_/datasets/nuscenes-mv3d-10class.py](../../configs/_base_/datasets/nuscenes-mv3d-10class.py) | Repository configuration or supporting asset: nuscenes-mv3d-10class.py. |
| [configs/_base_/default_runtime.py](../../configs/_base_/default_runtime.py) | Repository configuration or supporting asset: default_runtime.py. |
| [configs/_base_/models/fcos3d.py](../../configs/_base_/models/fcos3d.py) | Repository configuration or supporting asset: fcos3d.py. |
| [configs/_base_/models/multiview_dfm.py](../../configs/_base_/models/multiview_dfm.py) | Repository configuration or supporting asset: multiview_dfm.py. |
| [configs/_base_/models/pgd.py](../../configs/_base_/models/pgd.py) | Repository configuration or supporting asset: pgd.py. |
| [configs/_base_/schedules/cosine.py](../../configs/_base_/schedules/cosine.py) | Repository configuration or supporting asset: cosine.py. |
| [configs/_base_/schedules/cyclic-20e.py](../../configs/_base_/schedules/cyclic-20e.py) | Repository configuration or supporting asset: cyclic-20e.py. |
| [configs/_base_/schedules/cyclic-40e.py](../../configs/_base_/schedules/cyclic-40e.py) | Repository configuration or supporting asset: cyclic-40e.py. |
| [configs/_base_/schedules/mmdet-schedule-1x.py](../../configs/_base_/schedules/mmdet-schedule-1x.py) | Repository configuration or supporting asset: mmdet-schedule-1x.py. |
| [configs/_base_/schedules/schedule-2x.py](../../configs/_base_/schedules/schedule-2x.py) | Repository configuration or supporting asset: schedule-2x.py. |
| [configs/_base_/schedules/schedule-3x.py](../../configs/_base_/schedules/schedule-3x.py) | Repository configuration or supporting asset: schedule-3x.py. |
| [configs/_base_/schedules/seg-cosine-100e.py](../../configs/_base_/schedules/seg-cosine-100e.py) | Repository configuration or supporting asset: seg-cosine-100e.py. |
| [configs/_base_/schedules/seg-cosine-150e.py](../../configs/_base_/schedules/seg-cosine-150e.py) | Repository configuration or supporting asset: seg-cosine-150e.py. |
| [configs/_base_/schedules/seg-cosine-200e.py](../../configs/_base_/schedules/seg-cosine-200e.py) | Repository configuration or supporting asset: seg-cosine-200e.py. |
| [configs/_base_/schedules/seg-cosine-50e.py](../../configs/_base_/schedules/seg-cosine-50e.py) | Repository configuration or supporting asset: seg-cosine-50e.py. |
| [configs/custom/fcos3d_custom_nuscenes_json.py](../../configs/custom/fcos3d_custom_nuscenes_json.py) | FCOS3D template for custom camera data in the NuScenes JSON schema. |
| [configs/custom/pgd_custom_nuscenes_json.py](../../configs/custom/pgd_custom_nuscenes_json.py) | PGD (FCOS3D++) template for custom NuScenes-schema JSON data. |
| [configs/fcos3d/README.md](../../configs/fcos3d/README.md) | Documentation: FCOS3D: Fully Convolutional One-Stage Monocular 3D Object Detection |
| [configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py](../../configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py) | Repository configuration or supporting asset: fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py. |
| [configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d_finetune.py](../../configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d_finetune.py) | Repository configuration or supporting asset: fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d_finetune.py. |
| [configs/fcos3d/metafile.yml](../../configs/fcos3d/metafile.yml) | Model metadata and recipe/result references. |
| [configs/mvfcos3d/README.md](../../configs/mvfcos3d/README.md) | Documentation: NuScenes camera-only MV-FCOS3D |
| [configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py](../../configs/mvfcos3d/multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py) | Repository configuration or supporting asset: multiview-fcos3d_r101-dcn_1xb1_nuscenes-3d-10class.py. |
| [configs/pgd/README.md](../../configs/pgd/README.md) | Documentation: PGD (FCOS3D++) on nuScenes |
| [configs/pgd/metafile.yml](../../configs/pgd/metafile.yml) | Model metadata and recipe/result references. |
| [configs/pgd/pgd_mm3d_windows.py](../../configs/pgd/pgd_mm3d_windows.py) | Repository configuration or supporting asset: pgd_mm3d_windows.py. |
| [configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py](../../configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py) | Repository configuration or supporting asset: pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py. |
| [configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d_finetune.py](../../configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d_finetune.py) | Repository configuration or supporting asset: pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d_finetune.py. |

## demo

| File | Role or main definitions |
| --- | --- |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800.pkl](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800.pkl) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800.pkl. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_BACK_LEFT__1532402927647423.jpg](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_BACK_LEFT__1532402927647423.jpg) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__CAM_BACK_LEFT__1532402927647423.jpg. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_BACK_RIGHT__1532402927627893.jpg](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_BACK_RIGHT__1532402927627893.jpg) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__CAM_BACK_RIGHT__1532402927627893.jpg. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_BACK__1532402927637525.jpg](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_BACK__1532402927637525.jpg) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__CAM_BACK__1532402927637525.jpg. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_FRONT_LEFT__1532402927604844.jpg](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_FRONT_LEFT__1532402927604844.jpg) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__CAM_FRONT_LEFT__1532402927604844.jpg. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_FRONT_RIGHT__1532402927620339.jpg](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_FRONT_RIGHT__1532402927620339.jpg) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__CAM_FRONT_RIGHT__1532402927620339.jpg. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_FRONT__1532402927612460.jpg](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__CAM_FRONT__1532402927612460.jpg) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__CAM_FRONT__1532402927612460.jpg. |
| [demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin](../../demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin) | Repository configuration or supporting asset: n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin. |
| [demo/mono_det_demo.py](../../demo/mono_det_demo.py) | Defines parse_args, main. |

## docker

| File | Role or main definitions |
| --- | --- |
| [docker/Dockerfile](../../docker/Dockerfile) | Retained container or serving configuration; compatibility needs verification. |
| [docker/serve/Dockerfile](../../docker/serve/Dockerfile) | Retained container or serving configuration; compatibility needs verification. |
| [docker/serve/config.properties](../../docker/serve/config.properties) | Retained container or serving configuration; compatibility needs verification. |
| [docker/serve/entrypoint.sh](../../docker/serve/entrypoint.sh) | Retained container or serving configuration; compatibility needs verification. |

## docs

| File | Role or main definitions |
| --- | --- |
| [docs/build_fcos3d_workflow_docx.py](../../docs/build_fcos3d_workflow_docx.py) | Defines set_font, set_style, label_para, parse_steps, page_number and additional helpers. |
| [docs/en/Makefile](../../docs/en/Makefile) | Repository configuration or supporting asset: Makefile. |
| [docs/en/_static/css/readthedocs.css](../../docs/en/_static/css/readthedocs.css) | Repository configuration or supporting asset: readthedocs.css. |
| [docs/en/_static/image/mmdet3d-logo.png](../../docs/en/_static/image/mmdet3d-logo.png) | Repository configuration or supporting asset: mmdet3d-logo.png. |
| [docs/en/advanced_guides/customize_dataset.md](../../docs/en/advanced_guides/customize_dataset.md) | Documentation: Customize Datasets |
| [docs/en/advanced_guides/customize_models.md](../../docs/en/advanced_guides/customize_models.md) | Documentation: Customize Models |
| [docs/en/advanced_guides/customize_runtime.md](../../docs/en/advanced_guides/customize_runtime.md) | Documentation: Customize Runtime Settings |
| [docs/en/advanced_guides/datasets/index.rst](../../docs/en/advanced_guides/datasets/index.rst) | Documentation: :maxdepth: 3 |
| [docs/en/advanced_guides/datasets/kitti.md](../../docs/en/advanced_guides/datasets/kitti.md) | Documentation: KITTI Dataset |
| [docs/en/advanced_guides/datasets/lyft.md](../../docs/en/advanced_guides/datasets/lyft.md) | Documentation: Lyft Dataset |
| [docs/en/advanced_guides/datasets/nuscenes.md](../../docs/en/advanced_guides/datasets/nuscenes.md) | Documentation: NuScenes Dataset |
| [docs/en/advanced_guides/datasets/s3dis.md](../../docs/en/advanced_guides/datasets/s3dis.md) | Documentation: S3DIS Dataset |
| [docs/en/advanced_guides/datasets/scannet.md](../../docs/en/advanced_guides/datasets/scannet.md) | Documentation: ScanNet Dataset |
| [docs/en/advanced_guides/datasets/semantickitti.md](../../docs/en/advanced_guides/datasets/semantickitti.md) | Documentation: SemanticKITTI Dataset |
| [docs/en/advanced_guides/datasets/sunrgbd.md](../../docs/en/advanced_guides/datasets/sunrgbd.md) | Documentation: SUN RGB-D Dataset |
| [docs/en/advanced_guides/datasets/waymo.md](../../docs/en/advanced_guides/datasets/waymo.md) | Documentation: Waymo Dataset |
| [docs/en/advanced_guides/index.rst](../../docs/en/advanced_guides/index.rst) | Documentation: Datasets |
| [docs/en/advanced_guides/pure_point_cloud_dataset.md](../../docs/en/advanced_guides/pure_point_cloud_dataset.md) | Documentation: Use Pure Point Cloud Dataset |
| [docs/en/advanced_guides/supported_tasks/index.rst](../../docs/en/advanced_guides/supported_tasks/index.rst) | Documentation: :maxdepth: 1 |
| [docs/en/advanced_guides/supported_tasks/lidar_det3d.md](../../docs/en/advanced_guides/supported_tasks/lidar_det3d.md) | Documentation: LiDAR-Based 3D Detection |
| [docs/en/advanced_guides/supported_tasks/lidar_sem_seg3d.md](../../docs/en/advanced_guides/supported_tasks/lidar_sem_seg3d.md) | Documentation: LiDAR-Based 3D Semantic Segmentation |
| [docs/en/advanced_guides/supported_tasks/vision_det3d.md](../../docs/en/advanced_guides/supported_tasks/vision_det3d.md) | Documentation: Vision-Based 3D Detection |
| [docs/en/api.rst](../../docs/en/api.rst) | Documentation: mmdet3d.apis |
| [docs/en/conf.py](../../docs/en/conf.py) | Defines builder_inited_handler, setup. |
| [docs/en/get_started.md](../../docs/en/get_started.md) | Documentation: Get Started |
| [docs/en/index.rst](../../docs/en/index.rst) | Documentation: DeltaX India Camera-Based 3D Detection |
| [docs/en/make.bat](../../docs/en/make.bat) | Repository configuration or supporting asset: make.bat. |
| [docs/en/migration.md](../../docs/en/migration.md) | Documentation: Along with the release of OpenMMLab 2.0, MMDetection3D (namely MMDet3D) 1.1 made many significant changes, resulting in less redundant, more efficient code and  |
| [docs/en/model_zoo.md](../../docs/en/model_zoo.md) | Documentation: Model Zoo |
| [docs/en/notes/benchmarks.md](../../docs/en/notes/benchmarks.md) | Documentation: Benchmarks |
| [docs/en/notes/changelog.md](../../docs/en/notes/changelog.md) | Documentation: Changelog of v1.1 |
| [docs/en/notes/changelog_v1.0.x.md](../../docs/en/notes/changelog_v1.0.x.md) | Documentation: Changelog of v1.0.x |
| [docs/en/notes/compatibility.md](../../docs/en/notes/compatibility.md) | Documentation: Compatibility |
| [docs/en/notes/contribution_guides.md](../../docs/en/notes/contribution_guides.md) | Documentation: Contribution Guide |
| [docs/en/notes/faq.md](../../docs/en/notes/faq.md) | Documentation: FAQ |
| [docs/en/notes/index.rst](../../docs/en/notes/index.rst) | Documentation: :maxdepth: 1 |
| [docs/en/stat.py](../../docs/en/stat.py) | Repository configuration or supporting asset: stat.py. |
| [docs/en/switch_language.md](../../docs/en/switch_language.md) | Documentation page. |
| [docs/en/user_guides/backends_support.md](../../docs/en/user_guides/backends_support.md) | Documentation: Backends Support |
| [docs/en/user_guides/config.md](../../docs/en/user_guides/config.md) | Documentation: Learn about Configs |
| [docs/en/user_guides/coord_sys_tutorial.md](../../docs/en/user_guides/coord_sys_tutorial.md) | Documentation: Coordinate System |
| [docs/en/user_guides/data_pipeline.md](../../docs/en/user_guides/data_pipeline.md) | Documentation: Customize Data Pipelines |
| [docs/en/user_guides/dataset_prepare.md](../../docs/en/user_guides/dataset_prepare.md) | Documentation: Dataset Preparation |
| [docs/en/user_guides/fcos3d_datasets.md](../../docs/en/user_guides/fcos3d_datasets.md) | Documentation: FCOS3D dataset workflows |
| [docs/en/user_guides/fcos3d_nuscenes_validation.md](../../docs/en/user_guides/fcos3d_nuscenes_validation.md) | Documentation: FCOS3D NuScenes data generation and validation |
| [docs/en/user_guides/index.rst](../../docs/en/user_guides/index.rst) | Documentation: Train & Test |
| [docs/en/user_guides/inference.md](../../docs/en/user_guides/inference.md) | Documentation: Inference |
| [docs/en/user_guides/model_deployment.md](../../docs/en/user_guides/model_deployment.md) | Documentation: Model Deployment |
| [docs/en/user_guides/new_data_model.md](../../docs/en/user_guides/new_data_model.md) | Documentation: Train with Customized Datasets |
| [docs/en/user_guides/train_test.md](../../docs/en/user_guides/train_test.md) | Documentation: Test and Train on Standard Datasets |
| [docs/en/user_guides/useful_tools.md](../../docs/en/user_guides/useful_tools.md) | Documentation: We provide lots of useful tools under tools/ directory. |
| [docs/en/user_guides/visualization.md](../../docs/en/user_guides/visualization.md) | Documentation: Visualization |
| [docs/fcos3d_custom_nuscenes_data_requirements.md](../../docs/fcos3d_custom_nuscenes_data_requirements.md) | Documentation: Custom data requirements for camera-only FCOS3D |
| [docs/fcos3d_data_train_test_flow.svg](../../docs/fcos3d_data_train_test_flow.svg) | Repository configuration or supporting asset: fcos3d_data_train_test_flow.svg. |
| [docs/fcos3d_pkl_data_train_test_explained.docx](../../docs/fcos3d_pkl_data_train_test_explained.docx) | Repository configuration or supporting asset: fcos3d_pkl_data_train_test_explained.docx. |
| [docs/fcos3d_workflow_detailed.svg](../../docs/fcos3d_workflow_detailed.svg) | Repository configuration or supporting asset: fcos3d_workflow_detailed.svg. |
| [docs/fcos3d_workflow_full.svg](../../docs/fcos3d_workflow_full.svg) | Repository configuration or supporting asset: fcos3d_workflow_full.svg. |
| [docs/fcos3d_workflow_interactive.html](../../docs/fcos3d_workflow_interactive.html) | Repository configuration or supporting asset: fcos3d_workflow_interactive.html. |
| [docs/project/architecture.md](../../docs/project/architecture.md) | Documentation: Architecture and code ownership |
| [docs/project/data-preparation.md](../../docs/project/data-preparation.md) | Documentation: Data preparation and geometry contract |
| [docs/project/evaluation.md](../../docs/project/evaluation.md) | Documentation: Evaluation and visualization |
| [docs/project/file-inventory.md](../../docs/project/file-inventory.md) | Complete file inventory and role index (this document). |
| [docs/project/index.md](../../docs/project/index.md) | Documentation: DeltaX India project documentation |
| [docs/project/installation.md](../../docs/project/installation.md) | Documentation: Installation and environment verification |
| [docs/project/publication.md](../../docs/project/publication.md) | Documentation: Company publication and release checklist |
| [docs/project/repository-handbook.md](../../docs/project/repository-handbook.md) | Documentation: FCOS3D repository handbook |
| [docs/project/training.md](../../docs/project/training.md) | Documentation: Training, fine-tuning and continuation |
| [docs/project/troubleshooting.md](../../docs/project/troubleshooting.md) | Documentation: Troubleshooting and learning quality |
| [docs/project/validation.md](../../docs/project/validation.md) | Documentation: Validation evidence and result reporting |
| [docs/runn.md](../../docs/runn.md) | Documentation: Running the supported workflows |

## mmdet3d

| File | Role or main definitions |
| --- | --- |
| [mmdet3d/__init__.py](../../mmdet3d/__init__.py) | Package initialization, exports, or registration for mmdet3d. |
| [mmdet3d/datasets/__init__.py](../../mmdet3d/datasets/__init__.py) | Package initialization, exports, or registration for mmdet3d/datasets. |
| [mmdet3d/datasets/convert_utils.py](../../mmdet3d/datasets/convert_utils.py) | Defines get_nuscenes_2d_boxes, get_kitti_style_2d_boxes, convert_annos, post_process_coords, generate_record. |
| [mmdet3d/datasets/det3d_dataset.py](../../mmdet3d/datasets/det3d_dataset.py) | Defines Det3DDataset. |
| [mmdet3d/datasets/kitti2d_dataset.py](../../mmdet3d/datasets/kitti2d_dataset.py) | Defines Kitti2DDataset. |
| [mmdet3d/datasets/nuscenes_dataset.py](../../mmdet3d/datasets/nuscenes_dataset.py) | Defines NuScenesDataset. |
| [mmdet3d/datasets/nuscenes_json_dataset.py](../../mmdet3d/datasets/nuscenes_json_dataset.py) | NuScenes-format JSON loader for camera-only FCOS3D and PGD. |
| [mmdet3d/datasets/nuscenes_multiview_dataset.py](../../mmdet3d/datasets/nuscenes_multiview_dataset.py) | NuScenes camera-only dataset adapter for MV-FCOS3D++. |
| [mmdet3d/datasets/transforms/__init__.py](../../mmdet3d/datasets/transforms/__init__.py) | Package initialization, exports, or registration for mmdet3d/datasets/transforms. |
| [mmdet3d/datasets/transforms/data_augment_utils.py](../../mmdet3d/datasets/transforms/data_augment_utils.py) | Defines _rotation_box2d_jit_, box_collision_test, noise_per_box, noise_per_box_v2_, _select_transform and additional helpers. |
| [mmdet3d/datasets/transforms/formating.py](../../mmdet3d/datasets/transforms/formating.py) | Defines to_tensor, Pack3DDetInputs. |
| [mmdet3d/datasets/transforms/loading.py](../../mmdet3d/datasets/transforms/loading.py) | Defines LoadMultiViewImageFromFiles, LoadImageFromFileMono3D, LoadImageFromNDArray, LoadPointsFromMultiSweeps, PointSegClassMapping and additional helpers. |
| [mmdet3d/datasets/transforms/transforms_3d.py](../../mmdet3d/datasets/transforms/transforms_3d.py) | Defines RandomDropPointsColor, RandomFlip3D, RandomJitterPoints, ObjectSample, ObjectNoise and additional helpers. |
| [mmdet3d/datasets/utils.py](../../mmdet3d/datasets/utils.py) | Defines is_loading_function, get_loading_pipeline, convert_quaternion_to_matrix. |
| [mmdet3d/engine/__init__.py](../../mmdet3d/engine/__init__.py) | Package initialization, exports, or registration for mmdet3d/engine. |
| [mmdet3d/engine/hooks/__init__.py](../../mmdet3d/engine/hooks/__init__.py) | Package initialization, exports, or registration for mmdet3d/engine/hooks. |
| [mmdet3d/engine/hooks/numerical_debug_hook.py](../../mmdet3d/engine/hooks/numerical_debug_hook.py) | Fail at the first non-finite PGD training value with batch context. |
| [mmdet3d/engine/hooks/visualization_hook.py](../../mmdet3d/engine/hooks/visualization_hook.py) | Defines Det3DVisualizationHook. |
| [mmdet3d/evaluation/__init__.py](../../mmdet3d/evaluation/__init__.py) | Package initialization, exports, or registration for mmdet3d/evaluation. |
| [mmdet3d/evaluation/metrics/__init__.py](../../mmdet3d/evaluation/metrics/__init__.py) | Package initialization, exports, or registration for mmdet3d/evaluation/metrics. |
| [mmdet3d/evaluation/metrics/nuscenes_metric.py](../../mmdet3d/evaluation/metrics/nuscenes_metric.py) | Defines NuScenesMetric, output_to_nusc_box, lidar_nusc_box_to_global, cam_nusc_box_to_global, global_nusc_box_to_cam and additional helpers. |
| [mmdet3d/models/__init__.py](../../mmdet3d/models/__init__.py) | Package initialization, exports, or registration for mmdet3d/models. |
| [mmdet3d/models/data_preprocessors/__init__.py](../../mmdet3d/models/data_preprocessors/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/data_preprocessors. |
| [mmdet3d/models/data_preprocessors/data_preprocessor.py](../../mmdet3d/models/data_preprocessors/data_preprocessor.py) | Defines Det3DDataPreprocessor. |
| [mmdet3d/models/data_preprocessors/utils.py](../../mmdet3d/models/data_preprocessors/utils.py) | Defines multiview_img_stack_batch. |
| [mmdet3d/models/data_preprocessors/voxelize.py](../../mmdet3d/models/data_preprocessors/voxelize.py) | Defines _Voxelization, VoxelizationByGridShape, _DynamicScatter, DynamicScatter3D. |
| [mmdet3d/models/dense_heads/__init__.py](../../mmdet3d/models/dense_heads/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/dense_heads. |
| [mmdet3d/models/dense_heads/anchor3d_head.py](../../mmdet3d/models/dense_heads/anchor3d_head.py) | Defines Anchor3DHead. |
| [mmdet3d/models/dense_heads/anchor_free_mono3d_head.py](../../mmdet3d/models/dense_heads/anchor_free_mono3d_head.py) | Defines AnchorFreeMono3DHead. |
| [mmdet3d/models/dense_heads/base_3d_dense_head.py](../../mmdet3d/models/dense_heads/base_3d_dense_head.py) | Defines Base3DDenseHead. |
| [mmdet3d/models/dense_heads/base_mono3d_dense_head.py](../../mmdet3d/models/dense_heads/base_mono3d_dense_head.py) | Defines BaseMono3DDenseHead. |
| [mmdet3d/models/dense_heads/fcos_mono3d_head.py](../../mmdet3d/models/dense_heads/fcos_mono3d_head.py) | Defines FCOSMono3DHead. |
| [mmdet3d/models/dense_heads/nuscenes_velocity_anchor3d_head.py](../../mmdet3d/models/dense_heads/nuscenes_velocity_anchor3d_head.py) | A 9D Anchor3DHead variant for NuScenes velocity supervision. |
| [mmdet3d/models/dense_heads/pgd_head.py](../../mmdet3d/models/dense_heads/pgd_head.py) | Defines PGDHead. |
| [mmdet3d/models/dense_heads/train_mixins.py](../../mmdet3d/models/dense_heads/train_mixins.py) | Defines AnchorTrainMixin, get_direction_target. |
| [mmdet3d/models/detectors/__init__.py](../../mmdet3d/models/detectors/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/detectors. |
| [mmdet3d/models/detectors/dfm.py](../../mmdet3d/models/detectors/dfm.py) | Defines DfM. |
| [mmdet3d/models/detectors/fcos_mono3d.py](../../mmdet3d/models/detectors/fcos_mono3d.py) | Defines FCOSMono3D. |
| [mmdet3d/models/detectors/multiview_dfm.py](../../mmdet3d/models/detectors/multiview_dfm.py) | Defines MultiViewDfM. |
| [mmdet3d/models/detectors/single_stage_mono3d.py](../../mmdet3d/models/detectors/single_stage_mono3d.py) | Defines SingleStageMono3DDetector. |
| [mmdet3d/models/layers/__init__.py](../../mmdet3d/models/layers/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/layers. |
| [mmdet3d/models/layers/box3d_nms.py](../../mmdet3d/models/layers/box3d_nms.py) | Defines box3d_multiclass_nms, aligned_3d_nms, circle_nms, nms_bev, nms_normal_bev. |
| [mmdet3d/models/layers/fusion_layers/__init__.py](../../mmdet3d/models/layers/fusion_layers/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/layers/fusion_layers. |
| [mmdet3d/models/layers/fusion_layers/coord_transform.py](../../mmdet3d/models/layers/fusion_layers/coord_transform.py) | Defines apply_3d_transformation, extract_2d_info, bbox_2d_transform, coord_2d_transform. |
| [mmdet3d/models/layers/fusion_layers/point_fusion.py](../../mmdet3d/models/layers/fusion_layers/point_fusion.py) | Defines point_sample, PointFusion, voxel_sample. |
| [mmdet3d/models/mvfcos3d.py](../../mmdet3d/models/mvfcos3d.py) | Opt-in registrations for camera-only NuScenes MV-FCOS3D. |
| [mmdet3d/models/necks/__init__.py](../../mmdet3d/models/necks/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/necks. |
| [mmdet3d/models/necks/imvoxel_neck.py](../../mmdet3d/models/necks/imvoxel_neck.py) | Defines OutdoorImVoxelNeck, IndoorImVoxelNeck, ResModule. |
| [mmdet3d/models/task_modules/__init__.py](../../mmdet3d/models/task_modules/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/task_modules. |
| [mmdet3d/models/task_modules/anchor/__init__.py](../../mmdet3d/models/task_modules/anchor/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/task_modules/anchor. |
| [mmdet3d/models/task_modules/anchor/anchor_3d_generator.py](../../mmdet3d/models/task_modules/anchor/anchor_3d_generator.py) | Defines Anchor3DRangeGenerator, AlignedAnchor3DRangeGenerator, AlignedAnchor3DRangeGeneratorPerCls. |
| [mmdet3d/models/task_modules/anchor/builder.py](../../mmdet3d/models/task_modules/anchor/builder.py) | Defines build_prior_generator, build_anchor_generator. |
| [mmdet3d/models/task_modules/assigners/__init__.py](../../mmdet3d/models/task_modules/assigners/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/task_modules/assigners. |
| [mmdet3d/models/task_modules/assigners/max_3d_iou_assigner.py](../../mmdet3d/models/task_modules/assigners/max_3d_iou_assigner.py) | Defines Max3DIoUAssigner. |
| [mmdet3d/models/task_modules/builder.py](../../mmdet3d/models/task_modules/builder.py) | Defines build_assigner, build_sampler, build_bbox_coder. |
| [mmdet3d/models/task_modules/coders/__init__.py](../../mmdet3d/models/task_modules/coders/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/task_modules/coders. |
| [mmdet3d/models/task_modules/coders/delta_xyzwhlr_bbox_coder.py](../../mmdet3d/models/task_modules/coders/delta_xyzwhlr_bbox_coder.py) | Defines DeltaXYZWLHRBBoxCoder. |
| [mmdet3d/models/task_modules/coders/fcos3d_bbox_coder.py](../../mmdet3d/models/task_modules/coders/fcos3d_bbox_coder.py) | Defines FCOS3DBBoxCoder. |
| [mmdet3d/models/task_modules/coders/pgd_bbox_coder.py](../../mmdet3d/models/task_modules/coders/pgd_bbox_coder.py) | Defines PGDBBoxCoder. |
| [mmdet3d/models/task_modules/samplers/__init__.py](../../mmdet3d/models/task_modules/samplers/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/task_modules/samplers. |
| [mmdet3d/models/task_modules/samplers/pseudosample.py](../../mmdet3d/models/task_modules/samplers/pseudosample.py) | Defines PseudoSampler. |
| [mmdet3d/models/task_modules/voxel/__init__.py](../../mmdet3d/models/task_modules/voxel/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/task_modules/voxel. |
| [mmdet3d/models/task_modules/voxel/voxel_generator.py](../../mmdet3d/models/task_modules/voxel/voxel_generator.py) | Defines VoxelGenerator, points_to_voxel, _points_to_voxel_reverse_kernel, _points_to_voxel_kernel. |
| [mmdet3d/models/test_time_augs/__init__.py](../../mmdet3d/models/test_time_augs/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/test_time_augs. |
| [mmdet3d/models/test_time_augs/merge_augs.py](../../mmdet3d/models/test_time_augs/merge_augs.py) | Defines merge_aug_bboxes_3d. |
| [mmdet3d/models/utils/__init__.py](../../mmdet3d/models/utils/__init__.py) | Package initialization, exports, or registration for mmdet3d/models/utils. |
| [mmdet3d/models/utils/add_prefix.py](../../mmdet3d/models/utils/add_prefix.py) | Defines add_prefix. |
| [mmdet3d/models/utils/clip_sigmoid.py](../../mmdet3d/models/utils/clip_sigmoid.py) | Defines clip_sigmoid. |
| [mmdet3d/models/utils/edge_indices.py](../../mmdet3d/models/utils/edge_indices.py) | Defines get_edge_indices. |
| [mmdet3d/models/utils/gaussian.py](../../mmdet3d/models/utils/gaussian.py) | Defines gaussian_2d, draw_heatmap_gaussian, gaussian_radius, get_ellip_gaussian_2D, ellip_gaussian2D. |
| [mmdet3d/models/utils/gen_keypoints.py](../../mmdet3d/models/utils/gen_keypoints.py) | Defines get_keypoints. |
| [mmdet3d/models/utils/handle_objs.py](../../mmdet3d/models/utils/handle_objs.py) | Defines filter_outside_objs, get_centers2d_target, handle_proj_objs. |
| [mmdet3d/registry.py](../../mmdet3d/registry.py) | MMDetection3D provides 17 registry nodes to support using modules across |
| [mmdet3d/structures/__init__.py](../../mmdet3d/structures/__init__.py) | Package initialization, exports, or registration for mmdet3d/structures. |
| [mmdet3d/structures/bbox_3d/__init__.py](../../mmdet3d/structures/bbox_3d/__init__.py) | Package initialization, exports, or registration for mmdet3d/structures/bbox_3d. |
| [mmdet3d/structures/bbox_3d/base_box3d.py](../../mmdet3d/structures/bbox_3d/base_box3d.py) | Defines BaseInstance3DBoxes. |
| [mmdet3d/structures/bbox_3d/box_3d_mode.py](../../mmdet3d/structures/bbox_3d/box_3d_mode.py) | Defines Box3DMode. |
| [mmdet3d/structures/bbox_3d/cam_box3d.py](../../mmdet3d/structures/bbox_3d/cam_box3d.py) | Defines CameraInstance3DBoxes. |
| [mmdet3d/structures/bbox_3d/coord_3d_mode.py](../../mmdet3d/structures/bbox_3d/coord_3d_mode.py) | Defines Coord3DMode. |
| [mmdet3d/structures/bbox_3d/depth_box3d.py](../../mmdet3d/structures/bbox_3d/depth_box3d.py) | Defines DepthInstance3DBoxes. |
| [mmdet3d/structures/bbox_3d/lidar_box3d.py](../../mmdet3d/structures/bbox_3d/lidar_box3d.py) | Defines LiDARInstance3DBoxes. |
| [mmdet3d/structures/bbox_3d/utils.py](../../mmdet3d/structures/bbox_3d/utils.py) | Defines limit_period, rotation_3d_in_axis, xywhr2xyxyr, get_box_type, points_cam2img and additional helpers. |
| [mmdet3d/structures/det3d_data_sample.py](../../mmdet3d/structures/det3d_data_sample.py) | Defines Det3DDataSample. |
| [mmdet3d/structures/ops/__init__.py](../../mmdet3d/structures/ops/__init__.py) | Package initialization, exports, or registration for mmdet3d/structures/ops. |
| [mmdet3d/structures/ops/box_np_ops.py](../../mmdet3d/structures/ops/box_np_ops.py) | Defines camera_to_lidar, box_camera_to_lidar, corners_nd, center_to_corner_box2d, depth_to_points and additional helpers. |
| [mmdet3d/structures/ops/iou3d_calculator.py](../../mmdet3d/structures/ops/iou3d_calculator.py) | Defines BboxOverlapsNearest3D, BboxOverlaps3D, bbox_overlaps_nearest_3d, bbox_overlaps_3d, AxisAlignedBboxOverlaps3D and additional helpers. |
| [mmdet3d/structures/ops/transforms.py](../../mmdet3d/structures/ops/transforms.py) | Defines bbox3d_mapping_back, bbox3d2roi, bbox3d2result. |
| [mmdet3d/structures/point_data.py](../../mmdet3d/structures/point_data.py) | Defines PointData. |
| [mmdet3d/structures/points/__init__.py](../../mmdet3d/structures/points/__init__.py) | Package initialization, exports, or registration for mmdet3d/structures/points. |
| [mmdet3d/structures/points/base_points.py](../../mmdet3d/structures/points/base_points.py) | Defines BasePoints. |
| [mmdet3d/structures/points/cam_points.py](../../mmdet3d/structures/points/cam_points.py) | Defines CameraPoints. |
| [mmdet3d/structures/points/depth_points.py](../../mmdet3d/structures/points/depth_points.py) | Defines DepthPoints. |
| [mmdet3d/structures/points/lidar_points.py](../../mmdet3d/structures/points/lidar_points.py) | Defines LiDARPoints. |
| [mmdet3d/utils/__init__.py](../../mmdet3d/utils/__init__.py) | Package initialization, exports, or registration for mmdet3d/utils. |
| [mmdet3d/utils/array_converter.py](../../mmdet3d/utils/array_converter.py) | Defines array_converter, ArrayConverter. |
| [mmdet3d/utils/collect_env.py](../../mmdet3d/utils/collect_env.py) | Defines collect_env. |
| [mmdet3d/utils/compat_cfg.py](../../mmdet3d/utils/compat_cfg.py) | Defines compat_cfg, compat_runner_args, compat_imgs_per_gpu, compat_loader_args. |
| [mmdet3d/utils/misc.py](../../mmdet3d/utils/misc.py) | Defines replace_ceph_backend. |
| [mmdet3d/utils/setup_env.py](../../mmdet3d/utils/setup_env.py) | Defines setup_multi_processes, register_all_modules. |
| [mmdet3d/utils/typing_utils.py](../../mmdet3d/utils/typing_utils.py) | Collecting some commonly used type hint in MMDetection3D. |
| [mmdet3d/version.py](../../mmdet3d/version.py) | Defines parse_version_info. |
| [mmdet3d/visualization/__init__.py](../../mmdet3d/visualization/__init__.py) | Package initialization, exports, or registration for mmdet3d/visualization. |
| [mmdet3d/visualization/local_visualizer.py](../../mmdet3d/visualization/local_visualizer.py) | Defines Det3DLocalVisualizer. |
| [mmdet3d/visualization/vis_utils.py](../../mmdet3d/visualization/vis_utils.py) | Defines write_obj, write_oriented_bbox, to_depth_mode, proj_lidar_bbox3d_to_img, proj_depth_bbox3d_to_img and additional helpers. |

## requirements

| File | Role or main definitions |
| --- | --- |
| [requirements/build.txt](../../requirements/build.txt) | Dependency declarations for build. |
| [requirements/docs.txt](../../requirements/docs.txt) | Dependency declarations for docs. |
| [requirements/mminstall.txt](../../requirements/mminstall.txt) | Dependency declarations for mminstall. |
| [requirements/optional.txt](../../requirements/optional.txt) | Dependency declarations for optional. |
| [requirements/readthedocs.txt](../../requirements/readthedocs.txt) | Dependency declarations for readthedocs. |
| [requirements/runtime.txt](../../requirements/runtime.txt) | Dependency declarations for runtime. |
| [requirements/tests.txt](../../requirements/tests.txt) | Dependency declarations for tests. |

## resources

| File | Role or main definitions |
| --- | --- |
| [resources/browse_dataset_mono.png](../../resources/browse_dataset_mono.png) | Documentation image or visual example. |
| [resources/browse_dataset_multi_modality.png](../../resources/browse_dataset_multi_modality.png) | Documentation image or visual example. |
| [resources/browse_dataset_seg.png](../../resources/browse_dataset_seg.png) | Documentation image or visual example. |
| [resources/coord_sys_all.png](../../resources/coord_sys_all.png) | Documentation image or visual example. |
| [resources/data_pipeline.png](../../resources/data_pipeline.png) | Documentation image or visual example. |
| [resources/loss_curve.png](../../resources/loss_curve.png) | Documentation image or visual example. |
| [resources/mmdet3d-logo.png](../../resources/mmdet3d-logo.png) | Documentation image or visual example. |
| [resources/mmdet3d_outdoor_demo.gif](../../resources/mmdet3d_outdoor_demo.gif) | Documentation image or visual example. |
| [resources/nuimages_demo.gif](../../resources/nuimages_demo.gif) | Documentation image or visual example. |
| [resources/open3d_visual.gif](../../resources/open3d_visual.gif) | Documentation image or visual example. |
| [resources/open3d_visual.png](../../resources/open3d_visual.png) | Documentation image or visual example. |

## tests

| File | Role or main definitions |
| --- | --- |
| [tests/data/nuscenes/mono3d_sample_results.pkl](../../tests/data/nuscenes/mono3d_sample_results.pkl) | Small test fixture; not a full training dataset. |
| [tests/data/nuscenes/nus_info.pkl](../../tests/data/nuscenes/nus_info.pkl) | Small test fixture; not a full training dataset. |
| [tests/data/nuscenes/nus_infos_mono3d.coco.json](../../tests/data/nuscenes/nus_infos_mono3d.coco.json) | Small test fixture; not a full training dataset. |
| [tests/data/nuscenes/samples/CAM_BACK_LEFT/n015-2018-07-18-11-07-57+0800__CAM_BACK_LEFT__1531883530447423.jpg](../../tests/data/nuscenes/samples/CAM_BACK_LEFT/n015-2018-07-18-11-07-57+0800__CAM_BACK_LEFT__1531883530447423.jpg) | Small test fixture; not a full training dataset. |
| [tests/data/nuscenes/samples/LIDAR_TOP/n015-2018-08-02-17-16-37+0800__LIDAR_TOP__1533201470948018.pcd.bin](../../tests/data/nuscenes/samples/LIDAR_TOP/n015-2018-08-02-17-16-37+0800__LIDAR_TOP__1533201470948018.pcd.bin) | Small test fixture; not a full training dataset. |
| [tests/data/nuscenes/sweeps/LIDAR_TOP/n008-2018-09-18-12-07-26-0400__LIDAR_TOP__1537287083900561.pcd.bin](../../tests/data/nuscenes/sweeps/LIDAR_TOP/n008-2018-09-18-12-07-26-0400__LIDAR_TOP__1537287083900561.pcd.bin) | Small test fixture; not a full training dataset. |
| [tests/data/nuscenes/sweeps/LIDAR_TOP/n015-2018-08-02-17-16-37+0800__LIDAR_TOP__1533201470898274.pcd.bin](../../tests/data/nuscenes/sweeps/LIDAR_TOP/n015-2018-08-02-17-16-37+0800__LIDAR_TOP__1533201470898274.pcd.bin) | Small test fixture; not a full training dataset. |
| [tests/test_apis/test_inferencers/test_lidar_det3d_inferencer.py](../../tests/test_apis/test_inferencers/test_lidar_det3d_inferencer.py) | Tests: TestLidarDet3DInferencer. |
| [tests/test_apis/test_inferencers/test_lidar_seg3d_inferencer.py](../../tests/test_apis/test_inferencers/test_lidar_seg3d_inferencer.py) | Tests: TestLiDARSeg3DInferencer. |
| [tests/test_apis/test_inferencers/test_mono_det3d_inferencer.py](../../tests/test_apis/test_inferencers/test_mono_det3d_inferencer.py) | Tests: TestMonoDet3DInferencer. |
| [tests/test_apis/test_inferencers/test_multi_modality_det3d_inferencer.py](../../tests/test_apis/test_inferencers/test_multi_modality_det3d_inferencer.py) | Tests: TestMultiModalityDet3DInferencer. |
| [tests/test_datasets/test_dataset_wrappers.py](../../tests/test_datasets/test_dataset_wrappers.py) | Tests: TestCBGSDataset. |
| [tests/test_datasets/test_kitti_dataset.py](../../tests/test_datasets/test_kitti_dataset.py) | Tests: test_getitem. |
| [tests/test_datasets/test_lyft_dataset.py](../../tests/test_datasets/test_lyft_dataset.py) | Tests: test_getitem. |
| [tests/test_datasets/test_nuscenes_dataset.py](../../tests/test_datasets/test_nuscenes_dataset.py) | Tests: test_getitem. |
| [tests/test_datasets/test_nuscenes_pkl_camera_order.py](../../tests/test_datasets/test_nuscenes_pkl_camera_order.py) | Tests: test_v2_conversion_orders_images_and_camera_instances, test_v2_conversion_rejects_missing_camera. |
| [tests/test_datasets/test_s3dis_dataset.py](../../tests/test_datasets/test_s3dis_dataset.py) | Tests: TestS3DISDataset. |
| [tests/test_datasets/test_scannet_dataset.py](../../tests/test_datasets/test_scannet_dataset.py) | Tests: TestScanNetDataset. |
| [tests/test_datasets/test_semantickitti_dataset.py](../../tests/test_datasets/test_semantickitti_dataset.py) | Tests: TestSemanticKittiDataset. |
| [tests/test_datasets/test_sunrgbd_dataset.py](../../tests/test_datasets/test_sunrgbd_dataset.py) | Tests: TestScanNetDataset. |
| [tests/test_datasets/test_transforms/test_formating.py](../../tests/test_datasets/test_transforms/test_formating.py) | Tests: TestPack3DDetInputs. |
| [tests/test_datasets/test_transforms/test_loading.py](../../tests/test_datasets/test_transforms/test_loading.py) | Tests: TestLoadPointsFromFile, TestLoadAnnotations3D, TestPointSegClassMapping. |
| [tests/test_datasets/test_transforms/test_transforms_3d.py](../../tests/test_datasets/test_transforms/test_transforms_3d.py) | Tests: TestGlobalRotScaleTrans, TestRandomFlip3D, TestGlobalAlignment, TestPolarMix, and additional cases. |
| [tests/test_datasets/test_transforms/utils.py](../../tests/test_datasets/test_transforms/utils.py) | Tests: create_dummy_data_info, create_data_info_after_loading, create_mono3d_data_info_after_loading. |
| [tests/test_datasets/test_tta.py](../../tests/test_datasets/test_tta.py) | Tests: TestMuitiScaleFlipAug3D. |
| [tests/test_datasets/test_waymo_dataset.py](../../tests/test_datasets/test_waymo_dataset.py) | Tests: test_getitem. |
| [tests/test_engine/test_hooks/test_disable_object_sample_hook.py](../../tests/test_engine/test_hooks/test_disable_object_sample_hook.py) | Tests: TestDisableObjectSampleHook. |
| [tests/test_engine/test_hooks/test_numerical_debug_hook.py](../../tests/test_engine/test_hooks/test_numerical_debug_hook.py) | Tests: TestNumericalDebugHook. |
| [tests/test_engine/test_hooks/test_visualization_hook.py](../../tests/test_engine/test_hooks/test_visualization_hook.py) | Tests: TestVisualizationHook. |
| [tests/test_evaluation/test_functional/test_instance_seg_eval.py](../../tests/test_evaluation/test_functional/test_instance_seg_eval.py) | Tests: test_instance_seg_eval. |
| [tests/test_evaluation/test_functional/test_kitti_eval.py](../../tests/test_evaluation/test_functional/test_kitti_eval.py) | Tests: test_do_eval, test_kitti_eval, test_eval_class. |
| [tests/test_evaluation/test_functional/test_panoptic_seg_eval.py](../../tests/test_evaluation/test_functional/test_panoptic_seg_eval.py) | Tests: test_panoptic_seg_eval. |
| [tests/test_evaluation/test_functional/test_seg_eval.py](../../tests/test_evaluation/test_functional/test_seg_eval.py) | Tests: test_indoor_eval. |
| [tests/test_evaluation/test_metrics/test_indoor_metric.py](../../tests/test_evaluation/test_metrics/test_indoor_metric.py) | Tests: TestIndoorMetric. |
| [tests/test_evaluation/test_metrics/test_instance_seg_metric.py](../../tests/test_evaluation/test_metrics/test_instance_seg_metric.py) | Tests: TestInstanceSegMetric. |
| [tests/test_evaluation/test_metrics/test_kitti_metric.py](../../tests/test_evaluation/test_metrics/test_kitti_metric.py) | Tests: test_multi_modal_kitti_metric, test_kitti_metric_mAP. |
| [tests/test_evaluation/test_metrics/test_panoptic_seg_metric.py](../../tests/test_evaluation/test_metrics/test_panoptic_seg_metric.py) | Tests: TestPanopticSegMetric. |
| [tests/test_evaluation/test_metrics/test_seg_metric.py](../../tests/test_evaluation/test_metrics/test_seg_metric.py) | Tests: TestSegMetric. |
| [tests/test_models/test_backbones/test_cylinder3d_backbone.py](../../tests/test_models/test_backbones/test_cylinder3d_backbone.py) | Tests: test_cylinder3d. |
| [tests/test_models/test_backbones/test_dgcnn.py](../../tests/test_models/test_backbones/test_dgcnn.py) | Tests: test_dgcnn_gf. |
| [tests/test_models/test_backbones/test_dla.py](../../tests/test_models/test_backbones/test_dla.py) | Tests: test_dla_net. |
| [tests/test_models/test_backbones/test_mink_resnet.py](../../tests/test_models/test_backbones/test_mink_resnet.py) | Tests: test_mink_resnet. |
| [tests/test_models/test_backbones/test_minkunet_backbone.py](../../tests/test_models/test_backbones/test_minkunet_backbone.py) | Tests: test_minkunet_backbone. |
| [tests/test_models/test_backbones/test_multi_backbone.py](../../tests/test_models/test_backbones/test_multi_backbone.py) | Tests: test_multi_backbone. |
| [tests/test_models/test_backbones/test_pointnet2_sa_msg.py](../../tests/test_models/test_backbones/test_pointnet2_sa_msg.py) | Tests: test_pointnet2_sa_msg. |
| [tests/test_models/test_backbones/test_pointnet2_sa_ssg.py](../../tests/test_models/test_backbones/test_pointnet2_sa_ssg.py) | Tests: test_pointnet2_sa_ssg. |
| [tests/test_models/test_backbones/test_spvcnn_backbone.py](../../tests/test_models/test_backbones/test_spvcnn_backbone.py) | Tests: test_spvcnn_backbone. |
| [tests/test_models/test_data_preprocessors/test_data_preprocessor.py](../../tests/test_models/test_data_preprocessors/test_data_preprocessor.py) | Tests: TestDet3DDataPreprocessor. |
| [tests/test_models/test_decode_heads/test_cylinder3d_head.py](../../tests/test_models/test_decode_heads/test_cylinder3d_head.py) | Tests: TestCylinder3DHead. |
| [tests/test_models/test_decode_heads/test_dgcnn_head.py](../../tests/test_models/test_decode_heads/test_dgcnn_head.py) | Tests: TestDGCNNHead. |
| [tests/test_models/test_decode_heads/test_minkunet_head.py](../../tests/test_models/test_decode_heads/test_minkunet_head.py) | Tests: TestMinkUNetHead. |
| [tests/test_models/test_decode_heads/test_paconv_head.py](../../tests/test_models/test_decode_heads/test_paconv_head.py) | Tests: TestPAConvHead. |
| [tests/test_models/test_decode_heads/test_pointnet2_head.py](../../tests/test_models/test_decode_heads/test_pointnet2_head.py) | Tests: TestPointNet2Head. |
| [tests/test_models/test_dense_heads/test_anchor3d_head.py](../../tests/test_models/test_dense_heads/test_anchor3d_head.py) | Tests: TestAnchor3DHead. |
| [tests/test_models/test_dense_heads/test_fcaf3d_head.py](../../tests/test_models/test_dense_heads/test_fcaf3d_head.py) | Tests: TestFCAF3DHead. |
| [tests/test_models/test_dense_heads/test_fcos_mono3d_head.py](../../tests/test_models/test_dense_heads/test_fcos_mono3d_head.py) | Tests: TestFCOSMono3DHead. |
| [tests/test_models/test_dense_heads/test_freeanchors.py](../../tests/test_models/test_dense_heads/test_freeanchors.py) | Tests: TestFreeAnchor. |
| [tests/test_models/test_dense_heads/test_imvoxel_head.py](../../tests/test_models/test_dense_heads/test_imvoxel_head.py) | Tests: TestImVoxelHead. |
| [tests/test_models/test_dense_heads/test_monoflex_head.py](../../tests/test_models/test_dense_heads/test_monoflex_head.py) | Tests: TestMonoFlexHead. |
| [tests/test_models/test_dense_heads/test_pgd_head.py](../../tests/test_models/test_dense_heads/test_pgd_head.py) | Tests: TestFGDHead. |
| [tests/test_models/test_dense_heads/test_smoke_mono3d_head.py](../../tests/test_models/test_dense_heads/test_smoke_mono3d_head.py) | Tests: TestSMOKEMono3DHead. |
| [tests/test_models/test_dense_heads/test_ssn.py](../../tests/test_models/test_dense_heads/test_ssn.py) | Tests: TestSSN. |
| [tests/test_models/test_detectors/test_3dssd.py](../../tests/test_models/test_detectors/test_3dssd.py) | Tests: Test3DSSD. |
| [tests/test_models/test_detectors/test_center_point.py](../../tests/test_models/test_detectors/test_center_point.py) | Tests: TestCenterPoint. |
| [tests/test_models/test_detectors/test_fcaf3d.py](../../tests/test_models/test_detectors/test_fcaf3d.py) | Tests: TestFCAF3d. |
| [tests/test_models/test_detectors/test_groupfree3d.py](../../tests/test_models/test_detectors/test_groupfree3d.py) | Tests: TestGroupfree3d. |
| [tests/test_models/test_detectors/test_h3dnet.py](../../tests/test_models/test_detectors/test_h3dnet.py) | Tests: TestH3D. |
| [tests/test_models/test_detectors/test_imvotenet.py](../../tests/test_models/test_detectors/test_imvotenet.py) | Tests: TestImvoteNet. |
| [tests/test_models/test_detectors/test_imvoxelnet.py](../../tests/test_models/test_detectors/test_imvoxelnet.py) | Tests: TestImVoxelNet. |
| [tests/test_models/test_detectors/test_mvxnet.py](../../tests/test_models/test_detectors/test_mvxnet.py) | Tests: TestMVXNet. |
| [tests/test_models/test_detectors/test_parta2.py](../../tests/test_models/test_detectors/test_parta2.py) | Tests: TestPartA2. |
| [tests/test_models/test_detectors/test_pointrcnn.py](../../tests/test_models/test_detectors/test_pointrcnn.py) | Tests: TestPointRCNN. |
| [tests/test_models/test_detectors/test_pvrcnn.py](../../tests/test_models/test_detectors/test_pvrcnn.py) | Tests: TestPVRCNN. |
| [tests/test_models/test_detectors/test_sassd.py](../../tests/test_models/test_detectors/test_sassd.py) | Tests: TestSDSSD. |
| [tests/test_models/test_detectors/test_votenet.py](../../tests/test_models/test_detectors/test_votenet.py) | Tests: TestVotenet. |
| [tests/test_models/test_detectors/test_voxelnet.py](../../tests/test_models/test_detectors/test_voxelnet.py) | Tests: TestVoxelNet. |
| [tests/test_models/test_layers/test_box3d_nms.py](../../tests/test_models/test_layers/test_box3d_nms.py) | Tests: test_aligned_3d_nms, test_circle_nms, test_nms_bev, test_nms_normal_bev. |
| [tests/test_models/test_layers/test_dgcnn_modules/test_dgcnn_fa_module.py](../../tests/test_models/test_layers/test_dgcnn_modules/test_dgcnn_fa_module.py) | Tests: test_dgcnn_fa_module. |
| [tests/test_models/test_layers/test_dgcnn_modules/test_dgcnn_fp_module.py](../../tests/test_models/test_layers/test_dgcnn_modules/test_dgcnn_fp_module.py) | Tests: test_dgcnn_fp_module. |
| [tests/test_models/test_layers/test_dgcnn_modules/test_dgcnn_gf_module.py](../../tests/test_models/test_layers/test_dgcnn_modules/test_dgcnn_gf_module.py) | Tests: test_dgcnn_gf_module. |
| [tests/test_models/test_layers/test_fusion_layers/test_fusion_coord_trans.py](../../tests/test_models/test_layers/test_fusion_layers/test_fusion_coord_trans.py) | Tests: test_coords_transformation. |
| [tests/test_models/test_layers/test_fusion_layers/test_point_fusion.py](../../tests/test_models/test_layers/test_fusion_layers/test_point_fusion.py) | Tests: test_sample_single. |
| [tests/test_models/test_layers/test_fusion_layers/test_vote_fusion.py](../../tests/test_models/test_layers/test_fusion_layers/test_vote_fusion.py) | Tests: test_vote_fusion. |
| [tests/test_models/test_layers/test_minkowski_engine/test_minkowski_engine_module.py](../../tests/test_models/test_layers/test_minkowski_engine/test_minkowski_engine_module.py) | Tests: test_MinkowskiConvModule, test_MinkowskiResidualBlock. |
| [tests/test_models/test_layers/test_paconv/test_paconv_modules.py](../../tests/test_models/test_layers/test_paconv/test_paconv_modules.py) | Tests: test_paconv_sa_module_msg, test_paconv_sa_module, test_paconv_cuda_sa_module_msg, test_paconv_cuda_sa_module. |
| [tests/test_models/test_layers/test_paconv/test_paconv_ops.py](../../tests/test_models/test_layers/test_paconv/test_paconv_ops.py) | Tests: test_paconv, test_paconv_cuda. |
| [tests/test_models/test_layers/test_pointnet_modules/test_point_fp_module.py](../../tests/test_models/test_layers/test_pointnet_modules/test_point_fp_module.py) | Tests: test_pointnet_fp_module. |
| [tests/test_models/test_layers/test_pointnet_modules/test_point_sa_module.py](../../tests/test_models/test_layers/test_pointnet_modules/test_point_sa_module.py) | Tests: test_pointnet_sa_module_msg, test_pointnet_sa_module. |
| [tests/test_models/test_layers/test_spconv/test_spconv_module.py](../../tests/test_models/test_layers/test_spconv/test_spconv_module.py) | Tests: test_SparseBasicBlock, test_make_sparse_convmodule. |
| [tests/test_models/test_layers/test_torchsparse/test_torchsparse_module.py](../../tests/test_models/test_layers/test_torchsparse/test_torchsparse_module.py) | Tests: test_TorchsparseConvModule, test_TorchsparseResidualBlock. |
| [tests/test_models/test_layers/test_vote_module.py](../../tests/test_models/test_layers/test_vote_module.py) | Tests: test_vote_module. |
| [tests/test_models/test_losses/test_chamfer_disrance.py](../../tests/test_models/test_losses/test_chamfer_disrance.py) | Tests: test_chamfer_disrance. |
| [tests/test_models/test_losses/test_multibin_loss.py](../../tests/test_models/test_losses/test_multibin_loss.py) | Tests: test_multibin_loss. |
| [tests/test_models/test_losses/test_paconv_regularization_loss.py](../../tests/test_models/test_losses/test_paconv_regularization_loss.py) | Tests: test_paconv_regularization_loss. |
| [tests/test_models/test_losses/test_rotated_iou_loss.py](../../tests/test_models/test_losses/test_rotated_iou_loss.py) | Tests: test_rotated_iou_3d_loss. |
| [tests/test_models/test_losses/test_uncertain_smooth_l1_loss.py](../../tests/test_models/test_losses/test_uncertain_smooth_l1_loss.py) | Tests: test_uncertain_smooth_l1_loss. |
| [tests/test_models/test_middle_encoders/test_sparse_encoders.py](../../tests/test_models/test_middle_encoders/test_sparse_encoders.py) | Tests: test_sparse_encoder, test_sparse_encoder_for_ssd. |
| [tests/test_models/test_middle_encoders/test_sparse_unet.py](../../tests/test_models/test_middle_encoders/test_sparse_unet.py) | Tests: test_SparseUNet. |
| [tests/test_models/test_mvfcos3d_nuscenes.py](../../tests/test_models/test_mvfcos3d_nuscenes.py) | Tests: test_config_and_guards, test_velocity_loss_and_prediction, test_dataset_uses_pkl_version_and_camera_order, test_multiview_detector_loss_and_predict. |
| [tests/test_models/test_necks/test_dla_neck.py](../../tests/test_models/test_necks/test_dla_neck.py) | Tests: test_dla_neck. |
| [tests/test_models/test_necks/test_imvoxel_neck.py](../../tests/test_models/test_necks/test_imvoxel_neck.py) | Tests: test_imvoxel_neck. |
| [tests/test_models/test_necks/test_pointnet2_fp_neck.py](../../tests/test_models/test_necks/test_pointnet2_fp_neck.py) | Tests: test_pointnet2_fp_neck. |
| [tests/test_models/test_necks/test_second_fpn.py](../../tests/test_models/test_necks/test_second_fpn.py) | Tests: test_secfpn, test_centerpoint_fpn. |
| [tests/test_models/test_segmentors/test_cylinder3d.py](../../tests/test_models/test_segmentors/test_cylinder3d.py) | Tests: TestCylinder3D. |
| [tests/test_models/test_segmentors/test_minkunet.py](../../tests/test_models/test_segmentors/test_minkunet.py) | Tests: TestMinkUNet. |
| [tests/test_models/test_segmentors/test_seg3d_tta_model.py](../../tests/test_models/test_segmentors/test_seg3d_tta_model.py) | Tests: TestSeg3DTTAModel. |
| [tests/test_models/test_task_modules/test_anchor/test_anchor_3d_generator.py](../../tests/test_models/test_task_modules/test_anchor/test_anchor_3d_generator.py) | Tests: test_anchor_3d_range_generator, test_aligned_anchor_generator, test_aligned_anchor_generator_per_cls. |
| [tests/test_models/test_task_modules/test_coders/test_anchor_free_box_coder.py](../../tests/test_models/test_task_modules/test_coders/test_anchor_free_box_coder.py) | Tests: test_anchor_free_box_coder. |
| [tests/test_models/test_task_modules/test_coders/test_centerpoint_bbox_coder.py](../../tests/test_models/test_task_modules/test_coders/test_centerpoint_bbox_coder.py) | Tests: test_centerpoint_bbox_coder. |
| [tests/test_models/test_task_modules/test_coders/test_fcos3d_bbox_coder.py](../../tests/test_models/test_task_modules/test_coders/test_fcos3d_bbox_coder.py) | Tests: test_fcos3d_bbox_coder. |
| [tests/test_models/test_task_modules/test_coders/test_monoflex_bbox_coder.py](../../tests/test_models/test_task_modules/test_coders/test_monoflex_bbox_coder.py) | Tests: test_monoflex_bbox_coder. |
| [tests/test_models/test_task_modules/test_coders/test_partial_bin_based_box_coder.py](../../tests/test_models/test_task_modules/test_coders/test_partial_bin_based_box_coder.py) | Tests: test_partial_bin_based_box_coder. |
| [tests/test_models/test_task_modules/test_coders/test_pgd_bbox_coder.py](../../tests/test_models/test_task_modules/test_coders/test_pgd_bbox_coder.py) | Tests: test_pgd_bbox_coder. |
| [tests/test_models/test_task_modules/test_coders/test_point_xyzwhlr_bbox_coder.py](../../tests/test_models/test_task_modules/test_coders/test_point_xyzwhlr_bbox_coder.py) | Tests: test_point_xyzwhlr_bbox_coder. |
| [tests/test_models/test_task_modules/test_coders/test_smoke_bbox_coder.py](../../tests/test_models/test_task_modules/test_coders/test_smoke_bbox_coder.py) | Tests: test_smoke_bbox_coder. |
| [tests/test_models/test_task_modules/test_samplers/test_iou_piecewise_sampler.py](../../tests/test_models/test_task_modules/test_samplers/test_iou_piecewise_sampler.py) | Tests: test_iou_piecewise_sampler. |
| [tests/test_models/test_task_modules/test_voxel/test_voxel_generator.py](../../tests/test_models/test_task_modules/test_voxel/test_voxel_generator.py) | Tests: test_voxel_generator. |
| [tests/test_models/test_utils/test_utils.py](../../tests/test_models/test_utils/test_utils.py) | Tests: test_gaussian, test_array_converter, test_points_img2cam, test_generate_edge_indices, and additional cases. |
| [tests/test_models/test_voxel_encoders/test_pillar_encoder.py](../../tests/test_models/test_voxel_encoders/test_pillar_encoder.py) | Tests: test_pillar_feature_net. |
| [tests/test_models/test_voxel_encoders/test_voxel_encoders.py](../../tests/test_models/test_voxel_encoders/test_voxel_encoders.py) | Tests: test_hard_simple_VFE, test_seg_VFE. |
| [tests/test_samples/parta2_roihead_inputs.npz](../../tests/test_samples/parta2_roihead_inputs.npz) | Small test fixture; not a full training dataset. |
| [tests/test_structures/test_bbox/test_box3d.py](../../tests/test_structures/test_bbox/test_box3d.py) | Tests: test_bbox3d_mapping_back, test_bbox3d2roi, test_base_boxes3d, test_lidar_boxes3d, and additional cases. |
| [tests/test_structures/test_bbox/test_coord_3d_mode.py](../../tests/test_structures/test_bbox/test_coord_3d_mode.py) | Tests: test_points_conversion, test_boxes_conversion. |
| [tests/test_structures/test_det3d_data_sample.py](../../tests/test_structures/test_det3d_data_sample.py) | Tests: TestDet3DDataSample. |
| [tests/test_structures/test_ops/test_box_np_ops.py](../../tests/test_structures/test_ops/test_box_np_ops.py) | Tests: test_camera_to_lidar, test_box_camera_to_lidar, test_corners_nd, test_center_to_corner_box2d, and additional cases. |
| [tests/test_structures/test_point_data.py](../../tests/test_structures/test_point_data.py) | Tests: TestPointData. |
| [tests/test_structures/test_points/test_base_points.py](../../tests/test_structures/test_points/test_base_points.py) | Tests: test_base_points. |
| [tests/test_structures/test_points/test_cam_points.py](../../tests/test_structures/test_points/test_cam_points.py) | Tests: test_cam_points, test_lidar_points. |
| [tests/test_structures/test_points/test_depth_points.py](../../tests/test_structures/test_points/test_depth_points.py) | Tests: test_depth_points. |
| [tests/test_utils/test_compat_cfg.py](../../tests/test_utils/test_compat_cfg.py) | Tests: test_compat_runner_args, test_compat_loader_args, test_compat_imgs_per_gpu. |
| [tests/test_utils/test_setup_env.py](../../tests/test_utils/test_setup_env.py) | Tests: test_register_all_modules, test_setup_multi_processes. |

## tools

| File | Role or main definitions |
| --- | --- |
| [tools/__init__.py](../../tools/__init__.py) | Package initialization, exports, or registration for tools. |
| [tools/check_mvfcos3d.py](../../tools/check_mvfcos3d.py) | One-batch camera-only MV training, prediction and evaluator smoke test. |
| [tools/create_data.py](../../tools/create_data.py) | Prepare NuScenes data for FCOS3D and related NuScenes models. |
| [tools/create_data.sh](../../tools/create_data.sh) | Shell entry point or automation wrapper. |
| [tools/dataset_converters/__init__.py](../../tools/dataset_converters/__init__.py) | Package initialization, exports, or registration for tools/dataset_converters. |
| [tools/dataset_converters/nuscenes_camera_order.py](../../tools/dataset_converters/nuscenes_camera_order.py) | Canonical six-camera order for NuScenes PKL preparation and MV-FCOS3D. |
| [tools/dataset_converters/nuscenes_converter.py](../../tools/dataset_converters/nuscenes_converter.py) | Defines _validate_nuscenes_metadata, create_nuscenes_infos, get_available_scenes, _fill_trainval_infos, obtain_sensor2top and additional helpers. |
| [tools/dataset_converters/update_infos_to_v2.py](../../tools/dataset_converters/update_infos_to_v2.py) | Convert the annotation pkl to the standard format in OpenMMLab V2.0. |
| [tools/dist_test.sh](../../tools/dist_test.sh) | Shell entry point or automation wrapper. |
| [tools/dist_train.sh](../../tools/dist_train.sh) | Shell entry point or automation wrapper. |
| [tools/finetune_fcos3d.py](../../tools/finetune_fcos3d.py) | Fine-tune FCOS3D with optional module freezing. |
| [tools/slurm_test.sh](../../tools/slurm_test.sh) | Shell entry point or automation wrapper. |
| [tools/slurm_train.sh](../../tools/slurm_train.sh) | Shell entry point or automation wrapper. |
| [tools/stich_backup.py](../../tools/stich_backup.py) | Make timestamp-aligned 2x3 NuScenes camera mosaics and an MP4 video. |
| [tools/stitch_nuscenes_cameras.py](../../tools/stitch_nuscenes_cameras.py) | Make timestamp-aligned 2x3 NuScenes camera mosaics and an MP4 video. |
| [tools/test.py](../../tools/test.py) | Defines validate_fcos3d_nuscenes_config, parse_args, trigger_visualization_hook, main. |
| [tools/train.py](../../tools/train.py) | Defines validate_fcos3d_nuscenes_config, configure_nuscenes_best_metric, parse_args, main. |
| [tools/validate_custom_nuscenes_json.py](../../tools/validate_custom_nuscenes_json.py) | Validate a custom NuScenes-format JSON manifest before training or test. |
| [tools/validate_fcos3d_nuscenes.py](../../tools/validate_fcos3d_nuscenes.py) | Validate nuScenes V2 annotations for camera-only FCOS3D and PGD. |

## Local and generated artifacts

| Location | Role |
| --- | --- |
| `checkpoints/` | Locally available pretrained mono weights; not included by this index. |
| `samplers/` | Existing train/validation annotation PKLs; inspect provenance and paths before reuse. |
| `work_dirs/` | Experiment logs, resolved configs, checkpoints, and exports. |
| `data/` | User-supplied sensor data, metadata, and generated annotation directories. |
| `.pytest_cache/`, `__pycache__/` | Generated test and Python caches. |
