import os
import shutil
from pathlib import Path
from tqdm import tqdm

class FolderManager:
    """
    이미지와 라벨을 동시에 수집하여 YOLO 표준 구조(images/, labels/)로 정리하는 클래스
    """
    def __init__(self, src_root, dst_root):
        self.src_root = Path(src_root)
        self.dst_root = Path(dst_root)
        
        # 이미지와 라벨 확장자 정의
        self.img_exts = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG']
        self.lbl_exts = ['.json', '.txt', '.xml']
        
        # 저장할 폴더 구조 생성 (YOLO 표준)
        self.dst_img_dir = self.dst_root / "images"
        self.dst_lbl_dir = self.dst_root / "labels"
        
        self.dst_img_dir.mkdir(parents=True, exist_ok=True)
        self.dst_lbl_dir.mkdir(parents=True, exist_ok=True)

    def _get_all_files(self):
        """모든 이미지와 라벨 파일을 한 번에 스캔"""
        all_files = []
        target_exts = self.img_exts + self.lbl_exts
        for ext in target_exts:
            all_files.extend(list(self.src_root.rglob(f"*{ext}")))
        return all_files

    def collect(self, rename_with_parent=True):
        """
        파일을 확장자에 따라 images/ 또는 labels/ 폴더로 이동
        """
        all_files = self._get_all_files()
        total_files = len(all_files)
        
        print(f"🔍 총 {total_files}개의 파일을 찾았습니다. 정리를 시작합니다.")
        
        counts = {"images": 0, "labels": 0, "errors": 0}

        for file_path in tqdm(all_files, desc="📦 데이터 통합 중", unit="file"):
            try:
                # 1. 파일명 결정 (중복 방지를 위해 부모 폴더명 조합 권장)
                if rename_with_parent:
                    new_name = f"{file_path.parent.name}_{file_path.name}"
                else:
                    new_name = file_path.name
                
                # 2. 확장자에 따라 저장 위치 결정
                ext = file_path.suffix.lower()
                if ext in self.img_exts:
                    target_path = self.dst_img_dir / new_name
                    counts["images"] += 1
                elif ext in self.lbl_exts:
                    target_path = self.dst_lbl_dir / new_name
                    counts["labels"] += 1
                else:
                    continue # 대상 외 확장자 무시

                # 3. 복사 실행
                shutil.copy2(file_path, target_path)
                
            except Exception as e:
                print(f"\n❌ 에러 발생 ({file_path.name}): {e}")
                counts["errors"] += 1

        print(f"\n✨ 수집 완료!")
        print(f"🖼️ 이미지: {counts['images']}개")
        print(f"📑 라벨: {counts['labels']}개")
        print(f"❌ 에러: {counts['errors']}개")
        print(f"📍 결과 경로: {self.dst_root}")

# --- 실행부 (main.py 예시) ---
if __name__ == "__main__":
    # AI-HUB 원본 데이터 경로
    SRC = r"/home/haggi/fire_detection_datasets/AI-HUB segmentation/raw"
    # 새로 모을 경로
    DST = r"/home/haggi/fire_detection_datasets/AI-HUB segmentation/my_datasets"

    manager = FolderManager(SRC, DST)
    # rename_with_parent=True를 해야 이미지-라벨 매칭이 깨지지 않고 중복도 방지됨
    manager.collect(rename_with_parent=True)