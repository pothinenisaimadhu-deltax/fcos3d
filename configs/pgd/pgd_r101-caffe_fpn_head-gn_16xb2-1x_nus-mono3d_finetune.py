_base_ = './pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py'
# model settings
model = dict(
    bbox_head=dict(debug_finite=True),
    train_cfg=dict(code_weight=[
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.05, 0.05, 0.2, 0.2, 0.2, 0.2
    ]))
# optimizer
optim_wrapper = dict(optimizer=dict(lr=2.5e-5))
load_from = 'work_dirs/pgd_nus_benchmark_1x/latest.pth'

log_processor = dict(by_epoch=True, window_size=1)
default_hooks = dict(
    logger=dict(interval=1),
    checkpoint=dict(
        interval=1, max_keep_ckpts=3, save_last=True,
        save_best='auto', rule='greater'))
custom_hooks = [dict(type='NumericalDebugHook', detect_anomaly=True)]
