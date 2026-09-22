"""PGD (FCOS3D++) template for custom NuScenes-schema JSON data."""
_base_ = '../pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py'

data_root = 'data/custom/'
dataset_type = 'NuScenesJsonDataset'
model = dict(bbox_head=dict(debug_finite=True))
train_dataloader = dict(dataset=dict(
    type=dataset_type, data_root=data_root, ann_file='custom_train.json'))
val_dataloader = dict(dataset=dict(
    type=dataset_type, data_root=data_root, ann_file='custom_val.json'))
test_dataloader = val_dataloader
val_evaluator = dict(
    type='DumpResults', out_file_path='work_dirs/custom_pgd_val_predictions.pkl')
test_evaluator = val_evaluator

log_processor = dict(by_epoch=True, window_size=1)
default_hooks = dict(
    logger=dict(interval=1),
    checkpoint=dict(
        interval=1, max_keep_ckpts=3, save_last=True,
        save_best='auto', rule='greater'))
custom_hooks = [dict(type='NumericalDebugHook', detect_anomaly=True)]
