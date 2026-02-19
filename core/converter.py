import json
import yaml
from pathlib import Path
from tqdm import tqdm # tqdm 추가

class Converter:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.cfg = yaml.safe_load(f)
        
        self.raw_dir = Path(self.cfg['path']['raw_labels'])
        self.save_dir = Path(self.cfg['path']['output_dir'])
        self.class_map = self.cfg['class_mapping']
        self.mode = self.cfg['mode']

        self.save_dir.mkdir(parents=True, exist_ok=True)

    def process_all(self):
        json_files = list(self.raw_dir.glob("*.json"))
        
        # tqdm 적용: desc로 현재 모드(seg/box) 표시
        for j_path in tqdm(json_files, desc=f"📝 YOLO {self.mode} 변환 중", unit="file"):
            self._convert_single(j_path)
            
        print(f"\n✅ 변환 완료! 결과물 확인: {self.save_dir}")

    def _convert_single(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        img_w = data['images'][0]['width']
        img_h = data['images'][0]['height']
        
        results = []
        for ann in data['annotations']:
            orig_id = ann['category_id']
            
            # 클래스 필터링 및 매핑
            if orig_id not in self.class_map:
                continue
            new_id = self.class_map[orig_id]

            if self.mode == "seg":
                line = self._to_seg(new_id, ann['segmentation'][0], img_w, img_h)
            else:
                line = self._to_box(new_id, ann['bbox'], img_w, img_h)
            
            results.append(line)

        # 결과가 있을 때만 파일 생성 (이름 유지)
        if results:
            with open(self.save_dir / f"{json_path.stem}.txt", 'w') as f:
                f.write("\n".join(results))

    def _to_seg(self, cls_id, poly, w, h):
        """Polygon 좌표 정규화: [class_id x1 y1 x2 y2 ...]"""
        norm_coords = []
        for i in range(0, len(poly), 2):
            nx = min(max(poly[i] / w, 0.0), 1.0)      # 0~1 사이 클리핑
            ny = min(max(poly[i+1] / h, 0.0), 1.0)
            norm_coords.append(f"{nx:.6f} {ny:.6f}")
        return f"{cls_id} " + " ".join(norm_coords)

    def _to_box(self, cls_id, bbox, w, h):
        """Bbox 좌표 정규화: [class_id x_center y_center width height]"""
        # bbox: [xmin, ymin, w_box, h_box]
        xc = (bbox[0] + bbox[2] / 2) / w
        yc = (bbox[1] + bbox[3] / 2) / h
        bw = bbox[2] / w
        bh = bbox[3] / h
        return f"{cls_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}"