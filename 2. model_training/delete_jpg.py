import os

# JPG 파일과 PNG 파일이 저장된 디렉토리 경로 설정
jpg_dir = "G:/내 드라이브/006_BMS2/0002_latxray_training/dataset/non-aug/train/images"
png_dir = "G:/내 드라이브/006_BMS2/0002_latxray_training/dataset/non-aug/train/masks"

# JPG와 PNG 파일명을 저장할 세트
jpg_files = set()
png_files = set()

# JPG 디렉토리에서 파일명 추출 (확장자 제외)
for filename in os.listdir(jpg_dir):
    if filename.endswith(".jpg"):
        jpg_files.add(filename.split('.')[0])

# PNG 디렉토리에서 파일명 추출 (확장자 제외)
for filename in os.listdir(png_dir):
    if filename.endswith(".png"):
        # '_mask' 부분을 제거하여 파일명 저장
        png_files.add(filename.replace('_mask', '').split('.')[0])

# JPG 파일 중 PNG에 없는 파일 삭제
for jpg_file in jpg_files:
    if jpg_file not in png_files:
        jpg_file_path = os.path.join(jpg_dir, jpg_file + ".jpg")
        json_file_path = os.path.join(jpg_dir, jpg_file + ".json")
        
        # JPG 파일 삭제
        if os.path.exists(jpg_file_path):
            os.remove(jpg_file_path)
            print(f"Deleted: {jpg_file_path}")

        # JSON 파일 삭제
        if os.path.exists(json_file_path):
            os.remove(json_file_path)
            print(f"Deleted: {json_file_path}")
