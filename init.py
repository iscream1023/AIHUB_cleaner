# aihub_cleaner/__init__.py
import yaml
from core.Folder_manager import FolderManager
from core.deduplicator import Deduplicator
from core.converter import Converter
from core.sampler import Sampler

class AIHubPipeline:
    def __init__(self, config_path='./config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.cfg = yaml.safe_load(f)
        self.config_path = config_path

    def run(self):
        print("🔥 AI-HUB datasets cleaner ACTIVATED ")
        
        # Step 1: clean folder structure
        #fm = FolderManager(src_root=self.cfg['path']['src_root'], 
                           #dst_root=self.cfg['path']['dst_root'])
        #fm.collect(rename_with_parent=True)

        # Step 2: D-Hashing init
        #dedup = Deduplicator(img_dir=fm.dst_img_dir, 
                             #lbl_dir=fm.dst_lbl_dir, 
                             #hash_size=self.cfg['dedup'].get('hash_size', 8))
        
        # D-HASHING threshold 
        #dedup.run(threshold=self.cfg['dedup'].get('threshold', 2))

        # Step 3: CONVERT INTO YOLO FORMAT
        #converter = Converter(config_path=self.config_path)
        #converter.process_all()

        # 4. Sampling & YAML Generation (추가된 부분)
        sampler = Sampler(self.cfg)
        sampler.run()

        print("\n🚀 ALL PROCESS IS DONE")
