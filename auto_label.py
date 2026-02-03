import cv2
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

IMAGE_DIR = "dataset/images/train"
LABEL_DIR = "dataset/labels/train"

os.makedirs(LABEL_DIR, exist_ok=True)

for img_name in os.listdir(IMAGE_DIR):
    img_path = os.path.join(IMAGE_DIR, img_name)
    results = model(img_path)

    label_path = os.path.join(LABEL_DIR, img_name.replace(".jpg", ".txt"))

    with open(label_path, "w") as f:
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                x, y, w, h = box.xywhn[0]
                f.write(f"{cls} {x} {y} {w} {h}\n")
