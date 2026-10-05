_base_ = [
    '../_base_/datasets/nuscenes-mv3d-10class.py',
    '../_base_/models/multiview_dfm.py',
    '../_base_/default_runtime.py'
]
custom_imports = dict(imports=['mmdet3d.models.mvfcos3d'],
                      allow_failed_imports=False)

model = dict(
    # Twelve vertical cells reduce to 6 -> 3 -> 1 in OutdoorImVoxelNeck.
    voxel_size=(0.5, 0.5, 8. / 12.),
    anchor_generator=dict(ranges=[[-50., -50., -5., 50., 50., 3.]]),
    bbox_head_3d=dict(
        type='NuScenesVelocityAnchor3DHead', num_classes=10,
        bbox_coder=dict(type='DeltaXYZWLHRBBoxCoder', code_size=9),
        anchor_generator=dict(
            ranges=[[-50., -50., 0., 50., 50., 0.]] * 10,
            sizes=[
                [4.08, 1.73, 1.56], [10.5, 2.5, 3.5],
                [12.29, 2.9, 3.87], [6.93, 2.51, 3.44],
                [6.37, 2.85, 3.19], [1.70, 0.60, 1.28],
                [2.10, 0.77, 1.47], [0.73, 0.67, 1.77],
                [0.41, 0.41, 1.08], [2.50, 0.50, 0.98]
            ], rotations=[0., 1.57], reshape_out=False)),
    train_cfg=dict(
        code_weight=[1., 1., 1., 1., 1., 1., 1., 0.2, 0.2],
        assigner=[dict(
            type='Max3DIoUAssigner',
            iou_calculator=dict(type='BboxOverlapsNearest3D'),
            pos_iou_thr=0.5, neg_iou_thr=0.35, min_pos_iou=0.35,
            ignore_iof_thr=-1) for _ in range(10)]))

optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(type='AdamW', lr=0.0005, weight_decay=0.0001),
    paramwise_cfg=dict(custom_keys={'backbone': dict(lr_mult=0.1)}),
    clip_grad=dict(max_norm=35., norm_type=2))
param_scheduler = [
    dict(type='LinearLR', start_factor=1. / 3, by_epoch=False,
         begin=0, end=500),
    dict(type='MultiStepLR', begin=0, end=30, by_epoch=True,
         milestones=[20, 27], gamma=0.1)
]
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=30, val_interval=2)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
default_hooks = dict(checkpoint=dict(
    interval=1, save_last=True, max_keep_ckpts=3,
    save_best='NuScenes metric/pred_instances_3d_NuScenes/NDS',
    rule='greater'))
# spawn is supported on both Windows and Linux.
env_cfg = dict(mp_cfg=dict(mp_start_method='spawn', opencv_num_threads=0))
auto_scale_lr = dict(enable=False, base_batch_size=1)
find_unused_parameters = True
load_from = None
resume = False
