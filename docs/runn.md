• Run these from:

  cd C:\Users\saimadhu-deltax\code\fcos3d

  Use your environment Python, for example:

  C:\Users\saimadhu-deltax\code\mmdetection3d\mm3d\Scripts\python.exe

  Set a short alias first:

  $py = "C:\Users\saimadhu-deltax\code\mmdetection3d\mm3d\Scripts\python.exe"

  ### nuScenes FCOS3D
    
    & $py -m tools.create_data nuscenes `
    --root-path data/nuscenes `
    --out-dir data/nuscenes `
    --extra-tag nuscenes `
    --split-json data/nuscenes/v1.0-trainval/splits.json


  & $py -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/
  nuscenes --extra-tag nuscenes

  & $py tools/train.py configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-
  mono3d.py
  
  & $py tools/test.py configs/fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-
  mono3d.py work_dirs\YOUR_RUN\latest.pth

  ### nuScenes FCOS3D++ / PGD

  & $py -m tools.create_data nuscenes --root-path data/nuscenes --out-dir data/
  nuscenes --extra-tag nuscenes
  & $py tools/train.py configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py
  & $py tools/test.py configs/pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py
  work_dirs\YOUR_RUN\latest.pth

  ### KITTI PGD

  & $py tools/prepare_kitti_fcos3d.py --root-path data/kitti
  & $py tools/train.py configs/pgd/pgd_r101-caffe_fpn_head-gn_4xb3-4x_kitti-mono3d.py
  & $py tools/test.py configs/pgd/pgd_r101-caffe_fpn_head-gn_4xb3-4x_kitti-mono3d.py
  work_dirs\YOUR_RUN\latest.pth

  ### Custom JSON data — FCOS3D

  & $py tools/validate_custom_nuscenes_json.py data/custom/custom_train.json
  & $py tools/validate_custom_nuscenes_json.py data/custom/custom_val.json
  & $py tools/train.py configs/custom/fcos3d_custom_nuscenes_json.py
  & $py tools/test.py configs/custom/fcos3d_custom_nuscenes_json.py
  work_dirs\YOUR_RUN\latest.pth

  ### Custom JSON data — FCOS3D++ / PGD

  & $py tools/validate_custom_nuscenes_json.py data/custom/custom_train.json
  & $py tools/train.py configs/custom/pgd_custom_nuscenes_json.py
  & $py tools/test.py configs/custom/pgd_custom_nuscenes_json.py
  work_dirs\YOUR_RUN\latest.pth

  ### Native five-camera Waymo MV-FCOS3D++

  & $py tools/train.py configs/mvfcos3d/multiview-fcos3d_r101-dcn_8xb2_waymoD5-3d-
  3class.py --cfg-options load_from=PATH_TO_WAYMO_PGD_CHECKPOINT
  & $py tools/test.py configs/mvfcos3d/multiview-fcos3d_r101-dcn_8xb2_waymoD5-3d-
  3class.py work_dirs\YOUR_RUN\latest.pth

  ### nuScenes six-camera MV-FCOS3D++ template

  & $py tools/train.py configs/mvfcos3d/multiview-fcos3d_r101-dcn_nuscenes-6cam.py

  Do not run the last command until nuScenes 10-class anchor sizes, assigners, and
  voxel ranges are configured; it is currently an input-pipeline template.