"""Opt-in registrations for camera-only NuScenes MV-FCOS3D.

Keeping these imports out of the global model initializer leaves the existing
monocular workflows independent of the multi-view dependency path.
"""
from mmdet3d.datasets.nuscenes_multiview_dataset import NuScenesMultiViewDataset
from mmdet3d.datasets.transforms.loading import LoadMultiViewImageFromFiles
from mmdet3d.datasets.transforms.transforms_3d import (
    MultiViewWrapper, ObjectNameFilter, ObjectRangeFilter, RandomResize3D)
from .task_modules.anchor import AlignedAnchor3DRangeGenerator
from .task_modules.assigners import Max3DIoUAssigner
from .task_modules.coders.delta_xyzwhlr_bbox_coder import DeltaXYZWLHRBBoxCoder
from .necks.imvoxel_neck import OutdoorImVoxelNeck
from .dense_heads.nuscenes_velocity_anchor3d_head import NuScenesVelocityAnchor3DHead
from .detectors.multiview_dfm import MultiViewDfM
