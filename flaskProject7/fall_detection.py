import cv2
from ultralytics import YOLO
import time

model = YOLO('yolov8n.pt')

last_fall_time = 0
fall_cooldown = 5  # 跌倒检测的冷却时间（秒）


def can_emit_fall():
    global last_fall_time
    current_time = time.time()
    if current_time - last_fall_time >= fall_cooldown:
        last_fall_time = current_time
        return True
    return False


def detect_fall(frame):
    fall_detected = False
    results = model(frame, stream=True, classes=[0])  # 只检测人类

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            width = x2 - x1
            height = y2 - y1
            aspect_ratio = width / height

            if aspect_ratio > 2:  # 如果宽高比大于2，认为是跌倒
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Fall Detected", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                if can_emit_fall():
                    fall_detected = True
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return fall_detected, frame
