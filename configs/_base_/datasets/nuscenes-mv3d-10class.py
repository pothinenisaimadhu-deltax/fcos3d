# Camera-only input; GT boxes and calibration use the NuScenes LiDAR frame.
# No LiDAR point files are loaded. Use the updated frame-level info PKLs.
dataset_type = 'NuScenesMultiViewDataset'
data_root = 'data/nuscenes/'
backend_args = None
class_names = [
    'car', 'truck', 'trailer', 'bus', 'construction_vehicle', 'bicycle',
    'motorcycle', 'pedestrian', 'traffic_cone', 'barrier'
]
metainfo = dict(classes=class_names)
camera_names = [
    'CAM_FRONT_LEFT', 'CAM_FRONT', 'CAM_FRONT_RIGHT',
    'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT'
]
input_modality = dict(use_lidar=False, use_camera=True)
data_prefix = {camera: 'samples/' + camera for camera in camera_names}
point_cloud_range = [-50., -50., -5., 50., 50., 3.]

# Use a geometry-safe baseline before enabling additional augmentations.
# MultiViewDfM samples with ORIGINAL intrinsics plus per-view resize factors.
view_transforms = [
    dict(type='RandomResize3D', scale=(800, 450),
         ratio_range=(1., 1.), keep_ratio=True)
]
meta_keys = [
    'box_type_3d', 'img_shape', 'ori_shape', 'ori_cam2img', 'scale_factor',
    'flip', 'img_crop_offset', 'sample_idx', 'token', 'timestamp',
    'lidar2cam', 'num_ref_frames', 'num_views', 'ego2global'
]
image_loading = dict(
    type='LoadMultiViewImageFromFiles', to_float32=True, num_views=6,
    num_ref_frames=-1, backend_args=backend_args)
train_pipeline = [
    image_loading,
    dict(type='LoadAnnotations3D', with_bbox_3d=True, with_label_3d=True),
    dict(type='MultiViewWrapper', transforms=view_transforms),
    dict(type='ObjectRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='ObjectNameFilter', classes=class_names),
    dict(type='Pack3DDetInputs',
         keys=['img', 'gt_bboxes_3d', 'gt_labels_3d'], meta_keys=meta_keys)
]
test_pipeline = [
    image_loading,
    dict(type='MultiViewWrapper', transforms=view_transforms),
    dict(type='Pack3DDetInputs', keys=['img'], meta_keys=meta_keys)
]
train_dataloader = dict(
    batch_size=1, num_workers=2, persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type, data_root=data_root,
        ann_file='nuscenes_infos_train.pkl', data_prefix=data_prefix,
        pipeline=train_pipeline, modality=input_modality, test_mode=False,
        load_type='frame_based', box_type_3d='LiDAR', with_velocity=True,
        metainfo=metainfo, backend_args=backend_args))
val_dataloader = dict(
    batch_size=1, num_workers=1, persistent_workers=True, drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type, data_root=data_root,
        ann_file='nuscenes_infos_val.pkl', data_prefix=data_prefix,
        pipeline=test_pipeline, modality=input_modality, test_mode=True,
        load_type='frame_based', box_type_3d='LiDAR', with_velocity=True,
        metainfo=metainfo, backend_args=backend_args))
test_dataloader = val_dataloader
val_evaluator = dict(
    type='NuScenesMetric', data_root=data_root,
    ann_file=data_root + 'nuscenes_infos_val.pkl', metric='bbox',
    modality=input_modality, backend_args=backend_args)
test_evaluator = val_evaluator
