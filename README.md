# AI-HUB Cleaner: Automated Dataset Pipeline for On-Device AI

AI-HUB datasets are notorious for their fragmented folder structures, redundant video frames, and inconsistent label formats. AI-HUB Cleaner automates the tedious preprocessing steps, allowing researchers to focus on what truly matters: Model Architecture and Optimization.

🚀 Core Features

    Folder Flattening & Standardization: Automatically traverses deep, nested AI-HUB directories and collects files into a standardized YOLO structure (images/, labels/). It uses parent-folder prefixing to prevent filename collisions (e.g., FolderA_001.jpg, FolderB_001.jpg).

    Perceptual Hash (d-Hash) Deduplication: Removes redundant frames from video-extracted datasets using the d-Hash (Difference Hashing) algorithm. By adjusting the Hamming Distance threshold, you can eliminate near-identical frames to prevent model overfitting and reduce training time.

    YAML-Driven Configuration: Manage your entire pipeline via config.yaml. Switch between datasets, remap classes, or change conversion modes without touching a single line of code.

    High-Precision Smart Converter:

        Segmentation (Polygon): Normalizes and converts COCO-style polygons to YOLO Seg format.

        Detection (Bbox): Converts [xmin, ymin, w, h] to YOLO normalized [x_center, y_center, w, h].

        Class Mapping & Filtering: On-the-fly class merging (e.g., Black Smoke + White Smoke ➔ Smoke) and filtering of noise classes (e.g., Clouds, Fog).

    Progress Tracking: Integrated with tqdm for real-time monitoring of large-scale data processing.
### 🛠️ Installation
```markdown

# Install required dependencies

pip install PyYAML imagehash Pillow tqdm
```

### ⚙️ Configuration (config.yaml)
```
YAML

path:
  src_root: "path/to/raw/aihub/data"
  dst_root: "path/to/intermediate/flattened/data"
  raw_labels: "path/to/intermediate/flattened/data/labels"
  output_dir: "path/to/final/yolo/labels"


# Deduplication Settings

dedup:
  hash_size: 8
  threshold: 2  # Hamming distance (lower = stricter removal)

# Class Mapping (Original_ID: Target_ID)
# IDs not listed here will be automatically filtered out.
class_mapping:
  1: 1 # Black Smoke -> Smoke
  2: 1 # White Smoke -> Smoke
  3: 0 # Flame -> Fire

# Conversion Mode: "seg" or "box"
mode: "seg" 
```
# 📖 Usage

Execute the entire complex pipeline with just a few lines of code:
Python

from aihub_cleaner import AIHubPipeline

# Initialize and Run the Pipeline
pipeline = AIHubPipeline(config_path='config.yaml')
pipeline.run()

🛡️ License & Ethics

This tool is provided for research and development purposes. When using AI-HUB datasets, users must strictly adhere to the AI-HUB Terms of Use and Copyright Guidelines.
