import cv2
from ultralytics import YOLO

# Load YOLOv8 pretrained model
model = YOLO("yolov8n.pt")  # nano model (fast, CPU-friendly)

# Animals we want to detect
TARGET_ANIMALS = [
    "elephant",
    "bear",      # used as wild animal proxy
    "zebra",     # proxy
    "cow"        # wild boar proxy (YOLO lacks boar class)
]

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO inference
    results = model(frame)

    # Loop through detections
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label in TARGET_ANIMALS:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Label
                text = f"{label.upper()} {conf:.2f}"
                cv2.putText(frame, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Wild Animal Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
