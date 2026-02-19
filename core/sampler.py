import os
import shutil
import random
from pathlib import Path
from tqdm import tqdm
import yaml

class Sampler:
    def __init__(self, config):
        self.img_dir = Path(config['path']['dst_root']) / "images"
        self.lbl_dir = Path(config['path']['label_output_dir'])
        self.final_root = Path(config['path']['dst_root']).parent / "yolo_final"
        self.split_ratio = config.get('sampling', {}).get('split_ratio', 0.8)
        
        # 클래스 이름 정의 (config에서 가져오거나 기본값 사용)
        self.class_names = config.get('class_names', {0: 'fire', 1: 'smoke'})

    def run(self):
        print(f"🎯 최종 데이터셋 구축을 시작합니다. (비율 {self.split_ratio}:{1-self.split_ratio:.1f})")
        
        # 1. 짝이 맞는 파일 찾기
        pairs = []
        lbl_files = list(self.lbl_dir.glob("*.txt"))
        
        for lbl_path in tqdm(lbl_files, desc="🔗 이미지-라벨 매칭 확인 중"):
            # 이미지 확장자 후보들 (.jpg, .png, .jpeg)
            img_found = False
            for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG']:
                img_path = self.img_dir / f"{lbl_path.stem}{ext}"
                if img_path.exists():
                    pairs.append((img_path, lbl_path))
                    img_found = True
                    break
        
        print(f"✅ 총 {len(pairs)}개의 완벽한 짝을 찾았습니다.")

        # 2. 데이터 셔플 및 분할
        random.shuffle(pairs)
        split_idx = int(len(pairs) * self.split_ratio)
        train_data = pairs[:split_idx]
        val_data = pairs[split_idx:]

        # 3. 폴더 생성 및 복사
        for split in ['train', 'val']:
            (self.final_root / 'images' / split).mkdir(parents=True, exist_ok=True)
            (self.final_root / 'labels' / split).mkdir(parents=True, exist_ok=True)

        self._copy_files(train_data, 'train')
        self._copy_files(val_data, 'val')

        # 4. data.yaml 생성
        self._create_yaml()
        print(f"🚀 모든 준비가 끝났습니다! 경로: {self.final_root}")

    def _copy_files(self, data, split):
        for img_path, lbl_path in tqdm(data, desc=f"📦 {split} 데이터 복사 중"):
            shutil.copy2(img_path, self.final_root / 'images' / split / img_path.name)
            shutil.copy2(lbl_path, self.final_root / 'labels' / split / lbl_path.name)

    def _create_yaml(self):
        # 0번부터 순서대로 리스트 만들기
        names = [self.class_names[i] for i in sorted(self.class_names.keys())]
        
        data_yaml = {
            'train': str((self.final_root / 'images' / 'train').absolute()),
            'val': str((self.final_root / 'images' / 'val').absolute()),
            'nc': len(names),
            'names': names
        }
        
        yaml_path = self.final_root / 'data.yaml'
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data_yaml, f, allow_unicode=True, default_flow_style=False)