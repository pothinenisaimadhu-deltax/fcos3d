
import os
import sys
import json
import argparse
import mmengine
import shutil
import nuscenes.nuscenes
from tools.dataset_converters import nuscenes_converter as nuscenes_converter
from tools.dataset_converters.update_infos_to_v2 import update_pkl_infos
from tools.dataset_converters.create_gt_database import create_groundtruth_database

if __name__ == '__main__':
    from mmengine.registry import init_default_scope
    init_default_scope('mmdet3d')

    parser = argparse.ArgumentParser(
        description='Build custom NuScenes info and GT-database files.')
    parser.add_argument('--data-root', required=True)
    parser.add_argument('--output-root', required=True)
    parser.add_argument('--annotation-path', required=True)
    parser.add_argument('--calibration-path', required=True)
    parser.add_argument('--max-sweeps', type=int, default=10)
    parser.add_argument('--strip-sweeps', action='store_true')
    parser.add_argument('--train-scenes-file', required=True,
                        help='Text file containing one exact scene name per line.')
    parser.add_argument('--val-scenes-file', required=True,
                        help='Text file containing one exact scene name per line.')
    args = parser.parse_args()

    # These are the only runtime paths. There are intentionally no fallbacks.
    hdd_root = os.path.abspath(args.data_root)
    local_out_dir = os.path.abspath(args.output_root)
    local_annotation_path = os.path.abspath(args.annotation_path)
    local_calibration_path = os.path.abspath(args.calibration_path)
    STRIP_SWEEPS = args.strip_sweeps

    required_paths = {
        'data root': hdd_root,
        'annotation file': local_annotation_path,
        'calibration file': local_calibration_path,
        'metadata directory': os.path.join(hdd_root, 'v1.0-trainval'),
        'train scenes file': os.path.abspath(args.train_scenes_file),
        'val scenes file': os.path.abspath(args.val_scenes_file),
    }
    missing = [f'{label}: {path}' for label, path in required_paths.items()
               if not os.path.exists(path)]
    if missing:
        raise FileNotFoundError(
            'Required input path(s) do not exist; refusing to use a fallback:\n'
            + '\n'.join(missing))

    from nuscenes.utils import splits
    with open(os.path.abspath(args.train_scenes_file), 'r') as f:
        splits.train = [line.strip() for line in f if line.strip()]
    with open(os.path.abspath(args.val_scenes_file), 'r') as f:
        splits.val = [line.strip() for line in f if line.strip()]

    # Legacy server-path block removed; all paths come from argparse above.
    
    os.makedirs(local_out_dir, exist_ok=True)
    print(f"Target local output folder: {local_out_dir}")
    print(f"Using custom annotation file: {local_annotation_path}")
    print(f"Using custom calibration file: {local_calibration_path}")

    # Monkeypatch NuScenes reverse indexing for custom table records.
    original_make_reverse_index = nuscenes.nuscenes.NuScenes.__make_reverse_index__
    def safe_make_reverse_index(self, verbose: bool = True) -> None:
        for table_name in self.table_names:
            table = getattr(self, table_name, [])
            for member in table:
                if isinstance(member, dict) and 'token' not in member:
                    if 'sample_annotation_token' in member:
                        member['token'] = member['sample_annotation_token']
                    elif 'calibrated_sensor_token' in member:
                        member['token'] = member['calibrated_sensor_token']
        return original_make_reverse_index(self, verbose)

    nuscenes.nuscenes.NuScenes.__make_reverse_index__ = safe_make_reverse_index

    # 3. Monkeypatch NuScenes constructor to inject local files at runtime
    original_init = nuscenes.nuscenes.NuScenes.__init__
    def custom_nusc_init(self, version, dataroot, verbose=True, *args, **kwargs):
        original_init(self, version, dataroot, verbose, *args, **kwargs)
        
        has_updates = False
        
        # 2a. Inject local calibrations if they exist
        if os.path.exists(local_calibration_path):
            print(f"\n[*] Monkeypatch: Injecting local calibrations from: {local_calibration_path}")
            original_calibrated_sensors = {
                record['token']: record for record in self.calibrated_sensor
                if 'token' in record
            }
            with open(local_calibration_path, 'r') as f:
                calibrated_sensors = json.load(f)
            for record in calibrated_sensors:
                if 'token' not in record:
                    record['token'] = record.get('calibrated_sensor_token', '')
                if not record['token']:
                    raise ValueError(
                        'Each calibrated sensor record must contain token or '
                        'calibrated_sensor_token.')
            self.calibrated_sensor = calibrated_sensors
            custom_by_sensor = {
                record.get('sensor_token'): record['token']
                for record in calibrated_sensors
                if record.get('sensor_token')
            }
            # sample_data points to calibrated-sensor tokens. If the custom
            # calibration export generated new record tokens, relink those
            # references by the stable sensor_token.
            for sample_data in self.sample_data:
                old_cs = original_calibrated_sensors.get(
                    sample_data.get('calibrated_sensor_token'))
                sensor_token = old_cs.get('sensor_token') if old_cs else None
                if sensor_token in custom_by_sensor:
                    sample_data['calibrated_sensor_token'] = \
                        custom_by_sensor[sensor_token]
            has_updates = True
        else:
            print(f"\n[!] Warning: Local custom calibration file not found at {local_calibration_path}!")

        # 2b. Inject local annotations if they exist
        if os.path.exists(local_annotation_path):
            print(f"\n[*] Monkeypatch: Injecting local annotations from: {local_annotation_path}")
            with open(local_annotation_path, 'r') as f:
                raw_annotations = json.load(f)
            
            # Map category name to token using database categories
            cat_name_to_token = {cat['name']: cat['token'] for cat in self.category}
            default_cat_token = list(cat_name_to_token.values())[0] if cat_name_to_token else ""
            
            existing_instance_tokens = {inst['token'] for inst in self.instance}
            existing_attr_tokens = {attr['token'] for attr in self.attribute}
            existing_sample_tokens = {sample['token'] for sample in self.sample}
            
            seen_tokens = set()
            cleaned_annotations = []
            sample_annotation_tokens = {}
            for item in raw_annotations:
                token = item.get('sample_annotation_token', item.get('token'))
                if not token or token in seen_tokens:
                    continue
                
                # Filter out annotations referencing missing sample/frame tokens
                sample_token = item['sample_token']
                if sample_token not in existing_sample_tokens:
                    continue
                    
                seen_tokens.add(token)
                
                # Filter out invalid attribute tokens
                attr_tokens = item.get('attribute_tokens', [])
                if isinstance(attr_tokens, str):
                    attr_tokens = [attr_tokens]
                attr_tokens = [t for t in attr_tokens if t in existing_attr_tokens]
                
                # Dynamically generate missing instance records to prevent KeyError
                inst_token = item['instance_token']
                raw_category_name = item.get('category_name', '')
                category_name = raw_category_name.rsplit('.', 1)[-1]
                if inst_token not in existing_instance_tokens:
                    cat_token = cat_name_to_token.get(
                        raw_category_name,
                        cat_name_to_token.get(category_name, default_cat_token))
                    dummy_inst = {
                        'token': inst_token,
                        'category_token': cat_token,
                        'nbr_annotations': 1,
                        'first_annotation_token': token,
                        'last_annotation_token': token
                    }
                    self.instance.append(dummy_inst)
                    existing_instance_tokens.add(inst_token)

                nusc_ann = {
                    'token': token,
                    'sample_token': item['sample_token'],
                    'instance_token': inst_token,
                    'visibility_token': item.get('visibility_token', '4'),
                    'attribute_tokens': attr_tokens,
                    'translation': item['translation'],
                    'size': item['size'],
                    'rotation': item['rotation'],
                    'num_lidar_pts': item.get('num_lidar_pts', 0),
                    'num_radar_pts': item.get('num_radar_pts', 0),
                    'prev': item.get('prev', ''),
                    'next': item.get('next', '')
                }
                cleaned_annotations.append(nusc_ann)
                sample_annotation_tokens.setdefault(sample_token, []).append(token)
                
            self.sample_annotation = cleaned_annotations
            # sample.json still contains the original annotation tokens. Point
            # each sample to the exact custom tokens loaded above.
            for sample in self.sample:
                sample['anns'] = sample_annotation_tokens.get(sample['token'], [])
            has_updates = True
        else:
            print(f"\n[!] Warning: Local custom annotation file not found at {local_annotation_path}!")

        # 2c. Rebuild reverse indexes in devkit
        if has_updates:
            self.__make_reverse_index__(verbose)

    nuscenes.nuscenes.NuScenes.__init__ = custom_nusc_init

    # Optional: Monkeypatch DATASETS.build to strip LoadPointsFromMultiSweeps for datasets without sweeps
    if STRIP_SWEEPS:
        from mmdet3d.registry import DATASETS
        original_build = DATASETS.build
        def custom_build_dataset(cfg, *args, **kwargs):
            if isinstance(cfg, dict) and cfg.get('type') == 'NuScenesDataset':
                print("\n[*] Monkeypatch: Stripping LoadPointsFromMultiSweeps from dataset pipeline...")
                if 'pipeline' in cfg:
                    cfg['pipeline'] = [
                        t for t in cfg['pipeline'] 
                        if t.get('type') != 'LoadPointsFromMultiSweeps'
                    ]
            return original_build(cfg, *args, **kwargs)
        DATASETS.build = custom_build_dataset

    # 4. Step A: Run Raw Data Converter (reading HDD metadata but outputting locally)
    print("\n--- Phase 1: Running Data Converter ---")
    nuscenes_converter.create_nuscenes_infos(
        hdd_root,
        'nuscenes',
        version='v1.0-trainval',
        max_sweeps=args.max_sweeps,
        out_dir=local_out_dir)

    # 5. Step B: Explicitly convert the raw PKLs before building NuScenesDataset.
    print("\n--- Phase 2: Updating Pickles to v2 Format ---")
    train_pkl = os.path.join(local_out_dir, "nuscenes_infos_train.pkl")
    val_pkl = os.path.join(local_out_dir, "nuscenes_infos_val.pkl")
    update_pkl_infos(dataset='nuscenes', out_dir=local_out_dir,
                     pkl_path=train_pkl, data_root=hdd_root)
    update_pkl_infos(dataset='nuscenes', out_dir=local_out_dir,
                     pkl_path=val_pkl, data_root=hdd_root)

    # 6. Step C: Generate Ground Truth Database locally
    print("\n--- Phase 3: Generating Ground Truth Database ---")
    create_groundtruth_database(
        'NuScenesDataset', 
        hdd_root, # data_path (used to read points from HDD)
        'nuscenes', 
        info_path=train_pkl,
        database_save_path=os.path.join(local_out_dir, 'nuscenes_gt_database'),
        db_info_save_path=os.path.join(local_out_dir, 'nuscenes_dbinfos_train.pkl')
    )
    
    print("\nSetup finished! All outputs saved cleanly inside your local workspace. No HDD files changed.")
