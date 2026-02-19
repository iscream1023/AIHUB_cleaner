import os
from pathlib import Path
from PIL import Image
import imagehash  # pip install imagehash 필수
from tqdm import tqdm

class Deduplicator:
    """
    d-Hash 알고리즘을 사용하여 유사한 이미지를 찾아내고 제거하는 클래스
    """
    def __init__(self, img_dir, lbl_dir, hash_size=8):
        self.img_dir = Path(img_dir)
        self.lbl_dir = Path(lbl_dir)
        self.hash_size = hash_size
        self.hashes = {}  # {hash: file_name}

    def run(self, threshold=2):
        """
        중복 제거 실행
        threshold: 해시 값 차이(Hamming Distance). 0이면 완전 동일, 숫자가 커질수록 '비슷한' 것도 제거.
        """
        img_files = list(self.img_dir.glob("*"))
        print(f"🕵️ 중복 검사를 시작합니다. 대상: {len(img_files)}개")

        removed_count = 0
        
        for img_path in tqdm(img_files, desc="🔍 d-Hash 분석 중"):
            try:
                # 1. d-Hash 계산
                with Image.open(img_path) as img:
                    # dhash는 이미지의 인접 픽셀 밝기 차이를 이용함
                    current_hash = imagehash.dhash(img, hash_size=self.hash_size)
                
                # 2. 기존 해시들과 비교 (유사도 체크)
                is_duplicate = False
                for h, filename in self.hashes.items():
                    if current_hash - h <= threshold: # 해시 간 거리 계산
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    # 3. 중복이면 이미지와 대응하는 라벨 삭제
                    self._remove_pair(img_path)
                    removed_count += 1
                else:
                    # 4. 중복 아니면 해시 리스트에 추가
                    self.hashes[current_hash] = img_path.name
                    
            except Exception as e:
                print(f"❌ 오류 발생 ({img_path.name}): {e}")

        print(f"\n✨ 중복 제거 완료!")
        print(f"🗑️ 삭제된 데이터 세트(이미지+라벨): {removed_count}개")
        print(f"✅ 남은 고유 이미지: {len(self.hashes)}개")

    def _remove_pair(self, img_path):
        """이미지와 짝이 맞는 라벨 파일을 찾아 함께 삭제"""
        # 이미지 파일명에서 확장자만 떼어냄 (ex: fire_01.jpg -> fire_01)
        base_name = img_path.stem
        
        # 대응되는 라벨 파일 후보들 (json, txt 등)
        label_candidates = list(self.lbl_dir.glob(f"{base_name}.*"))
        
        # 이미지 삭제
        if img_path.exists():
            img_path.unlink()
            
        # 라벨 삭제
        for lbl in label_candidates:
            if lbl.exists():
                lbl.unlink()