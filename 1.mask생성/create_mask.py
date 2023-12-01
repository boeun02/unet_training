import json, os
import numpy as np
import cv2

# 로컬 환경에서 사용할 경로
path = r'C:\Users\qkrqh\OneDrive\바탕 화면\umm' #경로만 바꿔주면 어디서든 mask 생성 가능
jspath = os.listdir(path)
jspaths = sorted([os.path.join(path, f) for f in jspath if f.endswith('.json')])

# Update the Label_Class based on JSON annotations if needed
Label_Class = {
    'S1': 0, 'L5': 1, 'L4': 2, 'L3': 3, 'L2': 4, 'L1': 5,
    'T12': 6, 'T11': 7, 'T10': 8, 'T9': 9, 'latLSpine': 10, 'latSacrum': 11, 'Aorticcalcification': 12
}

# 각 클래스에 대한 색상을 정의합니다 (B, G, R 형식).
class_colors = {
    'S1': (255, 0, 0), 'L5': (0, 255, 0), 'L4': (0, 0, 255), 'L3': (255, 255, 0),
    'L2': (255, 0, 255), 'L1': (0, 255, 255), 'T12': (100, 100, 255),
    'T11': (100, 255, 100), 'T10': (255, 100, 100), 'T9': (100, 255, 255),
    'latLSpine': (255, 100, 255), 'latSacrum': (255, 255, 100), 'Aorticcalcification': (100, 100, 100)
}

# Ensure the 'mask' directory exists
mask_dir = os.path.join(path, "mask")
os.makedirs(mask_dir, exist_ok=True)

def convert_colored_mask(json_file, jpg_file, height, width, name):
    with open(json_file, 'r') as f:
        all_labels = json.load(f)

    if 'shapes' not in all_labels:
        print(f"'shapes' key not found in {json_file}")
        return

    maskImage = np.zeros((height, width, 3), dtype=np.uint8)  # RGB 채널을 사용합니다.

    for shape in all_labels['shapes']:
        label = shape['label']
        if label not in Label_Class:
            print(f"Label {label} not found in Label_Class dictionary")
            return
        points = [(int(point[0]), int(point[1])) for point in shape['points']]
        points_ = np.array(points, dtype=np.int32)
        
        # 클래스별로 정의된 색상을 사용하여 다각형을 채웁니다.
        cv2.fillPoly(maskImage, [points_], class_colors[label])

    savePath = os.path.join(mask_dir, name)
    success = cv2.imwrite(savePath, maskImage)
    if success:
        print(f"Saving colored mask image to: {savePath}")
    else:
        print(f"Failed to save colored mask image to {savePath}")

for json_file in jspaths:
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    jpg_file = os.path.join(path, base_name + '.jpg')
    mask_name = base_name + '_mask.png'

    if not os.path.exists(jpg_file):
        print(f"JPG file not found for {json_file}")
        continue

    img = cv2.imread(jpg_file)
    if img is not None:
        height, width, _ = img.shape
        convert_colored_mask(json_file, jpg_file, height, width, mask_name)
