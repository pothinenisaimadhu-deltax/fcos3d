"""FCOS3D template for custom camera data in the NuScenes JSON schema."""
_base_ = '../fcos3d/fcos3d_r101-caffe-dcn_fpn_head-gn_8xb2-1x_nus-mono3d.py'

data_root = 'data/custom/'
dataset_type = 'NuScenesJsonDataset'
train_dataloader = dict(dataset=dict(
    type=dataset_type, data_root=data_root, ann_file='custom_train.json'))
val_dataloader = dict(dataset=dict(
    type=dataset_type, data_root=data_root, ann_file='custom_val.json'))
test_dataloader = val_dataloader
val_evaluator = dict(
    type='DumpResults', out_file_path='work_dirs/custom_val_predictions.pkl')
test_evaluator = val_evaluator
