import cv2
import torch
from torchvision import transforms
from ultralytics import YOLO

# 加载预训练的YOLOv5模型
model = YOLO('yolov5s.pt')  # 你可以使用'yolov5n.pt'、'yolov5m.pt'等

def detect_person(frame, conf_threshold=0.5):
    results = model(frame)  # 使用YOLOv5模型进行检测

    boxes = []
    for result in results:
        for i, (bbox, score, cls) in enumerate(zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls)):
            if cls == 0 and score > conf_threshold:  # COCO数据集中人的类别ID为0
                x1, y1, x2, y2 = map(int, bbox)
                boxes.append((x1, y1, x2, y2))

                # 绘制边框和标签
                label = f'Person: {score:.2f}'
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绘制绿色边框
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return boxes
