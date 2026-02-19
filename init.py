# aihub_cleaner/__init__.py
import yaml
from core.Folder_manager import FolderManager
from core.deduplicator import Deduplicator
from core.converter import Converter

class AIHubPipeline:
    def __init__(self, config_path='./config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.cfg = yaml.safe_load(f)
        self.config_path = config_path

    def run(self):
        print("🔥 AI-HUB 전처리 파이프라인 가동 (버터플라이 모드)")
        
        # Step 1: 폴더 정리
        fm = FolderManager(src_root=self.cfg['path']['src_root'], 
                           dst_root=self.cfg['path']['dst_root'])
        fm.collect(rename_with_parent=True)

        # Step 2: 중복 제거 (해싱 유사도 설정 반영)
        dedup = Deduplicator(img_dir=fm.dst_img_dir, 
                             lbl_dir=fm.dst_lbl_dir, 
                             hash_size=self.cfg['dedup'].get('hash_size', 8))
        
        # 유사도 임계값(threshold) 전달
        dedup.run(threshold=self.cfg['dedup'].get('threshold', 2))

        # Step 3: YOLO 변환
        converter = Converter(config_path=self.config_path)
        converter.process_all()

        print("\n🚀 모든 공정이 끝났습니다. 이제 11s 깎으러 가십시오.")