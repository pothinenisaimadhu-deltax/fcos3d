_base_ = './fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py'
# Second stage of the published recipe: increase only the depth-loss weight.
# This config must be initialized from a checkpoint produced by the baseline.
model = dict(
    train_cfg=dict(
        code_weight=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.05, 0.05]))
# Use half the baseline LR for the depth-loss fine-tuning stage.
optim_wrapper = dict(optimizer=dict(lr=0.001))
# Supply the baseline checkpoint at launch, for example:
# --cfg-options load_from=work_dirs/fcos3d_nus_baseline/best_*.pth
# Do not initialize from the published *fine-tuned* checkpoint; that would
# invalidate this stage and make results impossible to reproduce.
load_from = None
