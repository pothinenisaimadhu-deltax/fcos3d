"""PGD (FCOS3D++) template for custom NuScenes-schema JSON data."""
_base_ = '../pgd/pgd_r101-caffe_fpn_head-gn_16xb2-1x_nus-mono3d.py'

data_root = 'data/custom/'
dataset_type = 'NuScenesJsonDataset'
train_dataloader = dict(dataset=dict(
    type=dataset_type, data_root=data_root, ann_file='custom_train.json'))
val_dataloader = dict(dataset=dict(
    type=dataset_type, data_root=data_root, ann_file='custom_val.json'))
test_dataloader = val_dataloader
val_evaluator = dict(
    type='DumpResults', out_file_path='work_dirs/custom_pgd_val_predictions.pkl')
test_evaluator = val_evaluator
