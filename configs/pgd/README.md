# PGD (FCOS3D++) on nuScenes

This repository supports PGD as its FCOS3D++ implementation, restricted to
the camera-only nuScenes workflow. It does not include the distinct multi-view
MV-FCOS3D++ Waymo implementation.

Prepare annotations with `python -m tools.create_data nuscenes`, then train or
evaluate with `configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py`.
For Windows single-GPU execution, use `configs/pgd/pgd_mm3d_windows.py`.
