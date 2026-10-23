# Lateral Lumbar X-ray Vertebra Segmentation (U-Net)

Multi-class semantic segmentation of vertebrae on lateral lumbar spine X-rays, built as a **model-assisted labeling pipeline**: a U-Net trained on manually annotated images generates draft annotations that annotators open and correct directly in their labeling tool.

Developed during a part-time AI developer role at a medical AI startup (Oct 2023 – Feb 2024).

> **Note:** Training images are not included because they are patient X-rays. Only code and working notes are published.

---

## Overview

| | |
|---|---|
| **Task** | 13-class semantic segmentation (per-pixel vertebra labeling) |
| **Input** | Lateral lumbar X-ray (original 3072 × 1996, resized to 384 × 256) |
| **Classes** | S1, L5, L4, L3, L2, L1, T12, T11, T10, T9, latLSpine, latSacrum, Aorticcalcification |
| **Data** | 581 training / 101 test images, polygon-annotated in labelme |
| **Model** | U-Net implemented from scratch (TensorFlow/Keras) |
| **Environment** | Google Colab (GPU) |

A YOLOv8-seg model was developed in parallel as an alternative approach ([yolo_for_latxray](https://github.com/boeun02/yolo_for_latxray)). Based on a qualitative comparison of the predicted masks, U-Net was selected and deployed.

## Pipeline

```
labelme polygon annotations (.json)
        ↓  1. mask generation
color-coded segmentation masks (.png)
        ↓  2. model training
U-Net (.h5)
        ↓  3. inference
per-class color masks + pixel-level class CSV
        ↓  4. annotation export
AnyLabeling-compatible .json  →  annotators review and correct
```

| Step | Folder | What it does |
|---|---|---|
| 1 | `1.mask생성/` | `create_mask.py` converts labelme polygons into RGB masks, one color per class |
| 2 | `2. model_training/` | U-Net training notebooks. `delete_jpg.py` removes images whose masks are missing so image/mask pairs stay aligned |
| 3 | `3. model로 color mask와 csv 생성/` | Inference: per-class colored masks, overlays, and a `(row, column, class)` CSV |
| 4 | `4. model로 json 파일 생성/` | Converts predicted masks into AnyLabeling-format JSON so predictions load as editable annotations |

Each folder contains a `.hwpx` working note (Korean) describing the step in detail.

## Model

Standard U-Net encoder–decoder with skip connections.

- **Encoder:** 4 blocks of (Conv → BatchNorm → ReLU) × 2 + MaxPool; 64 → 128 → 256 → 512 filters
- **Bridge:** 1024 filters
- **Decoder:** Conv2DTranspose upsampling + skip concatenation; 512 → 256 → 128 → 64 filters
- **Output:** 1×1 Conv, softmax over 13 classes

| Hyperparameter | Value |
|---|---|
| Optimizer | Adam, lr = 1e-4 |
| Loss | Sparse categorical cross-entropy |
| Batch size | 8 |
| Epochs | up to 100 |
| Callbacks | ModelCheckpoint, ReduceLROnPlateau, EarlyStopping, CSVLogger |

Two versions were developed:

- **ver1:** binary segmentation (spine vs. background). Produced fragmented masks and could not separate vertebra classes.
- **ver2:** 13-class segmentation. Enables per-class color masks, CSV export, and annotation export.

## Engineering notes

- **Resolution vs. memory:** Full-resolution training did not fit in available GPU memory. Reducing batch size preserves detail but slows training; reducing resolution saves memory at the cost of fine boundaries. Images were downscaled to 384 × 256 after batch-size reduction alone was not enough.
- **Annotation format compatibility:** The first JSON export failed to load in AnyLabeling because its schema differed from the tool's. The exporter was rewritten to match the AnyLabeling format so predictions open as editable polygons.
- **Data consistency:** Mismatched image/mask counts caused training errors, so a cleanup script aligns files by name before training.

## Limitations

- Evaluation was limited to pixel accuracy and loss curves. Pixel accuracy is dominated by background pixels in X-rays, so it overstates segmentation quality. Per-class **Dice / IoU** would be the appropriate metrics and were not computed.
- The gap between training loss (~0.03) and validation loss (~0.12) suggests overfitting on a small dataset. No data augmentation was used.
- Downscaling from 3072 × 1996 to 384 × 256 loses fine boundary detail, especially between adjacent vertebrae.
- Paths are hard-coded for Google Colab / Google Drive.

## Stack

Python · TensorFlow / Keras · OpenCV · NumPy · Google Colab · labelme · AnyLabeling
