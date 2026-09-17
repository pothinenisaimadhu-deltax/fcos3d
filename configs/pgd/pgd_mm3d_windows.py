_base_ = './pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py'

env_cfg = dict(mp_cfg=dict(mp_start_method='spawn'))
train_dataloader = dict(batch_size=1, num_workers=0, persistent_workers=False)
val_dataloader = dict(num_workers=0, persistent_workers=False)
test_dataloader = dict(num_workers=0, persistent_workers=False)
# Scale the original 32-image global batch learning rate to one image.
optim_wrapper = dict(optimizer=dict(lr=0.004 / 32))
