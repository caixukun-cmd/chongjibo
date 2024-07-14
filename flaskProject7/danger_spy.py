import time
import cv2
import torch
from ultralytics import YOLO

# 改成自己的yolov5的路径
model_1 = torch.hub.load('C:/Users/Mafu/PycharmProjects/yolov5-master', 'custom',
                       path='C:/Users/Mafu/PycharmProjects/flaskProject7/mymodel.pt', source='local')


# model = YOLO('yolov8s.pt')
last_danger_time = {}
danger_areas = {'stream_1': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0},
                'stream_2': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0},
                'stream_3': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0},
                'stream_4': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0},
                'stream_5': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0},
                'stream_6': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}}

last_fall_time = 0
fall_cooldown = 5  # 跌倒检测的冷却时间（秒）


def can_emit_fall():
    global last_fall_time
    current_time = time.time()
    if current_time - last_fall_time >= fall_cooldown:
        last_fall_time = current_time
        return True
    return False


def can_emit(stream_id):
    global last_danger_time
    current_time = time.time()
    if stream_id not in last_danger_time or current_time - last_danger_time[stream_id] >= 5:
        last_danger_time[stream_id] = current_time
        return True
    return False


def set_danger(stream_id, x1, y1, x2, y2):
    global danger_areas
    danger_areas[stream_id] = {
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2
    }


def in_danger(stream_id, x1, y1, x2, y2):
    area = danger_areas[stream_id]
    if area['x1'] < x2 < area['x2'] and area['y1'] < y2 < area['y2']:
        return True
    elif area['x1'] < x1 < area['x2'] and area['y1'] < y2 < area['y2']:
        return True
    else:
        return False


def danger_fall(frame, stream_id):
    is_danger = False
    fall_detected = False
    results = model_1(frame)  # 运行模型进行检测 # 如果使用的是 YOLOv5，results.xyxy[0] 包含了所有检测框
    detection_boxes = results.xyxy[0]  # 获取所有检测框
    tuilijieguo = []  # 用于存储图像的识别结果
    for box in detection_boxes:
        x1, y1, x2, y2, confidence, class_id = box.tolist()  # 解析每个检测框
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        label = model_1.names[int(class_id)]  # 获取类别名称
        similarity = f"{confidence:.2f}"  # 置信度格式化 # 检测跌倒（简单示例，根据宽高比）
        tuilijieguo.append({'类别': label, '相似度': similarity, '坐标': [x1, y1, x2, y2]})

    # 根据处理结果对图片进行标识
    if len(tuilijieguo) > 0:
        for item in tuilijieguo:
            coords = item['坐标']
            if in_danger(stream_id, *coords):
                cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 0, 255), 2)
                if can_emit(stream_id):
                    is_danger = True
            else:
                cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)

            if item['类别'] == 'fall':
                cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 255), 2)
                cv2.putText(frame, "Fall Detected", (coords[0], coords[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                if can_emit_fall():
                    fall_detected = True

    area = danger_areas[stream_id]
    cv2.rectangle(frame, (area['x1'], area['y1']), (area['x2'], area['y2']), (0, 0, 255), 2)
    return is_danger, fall_detected
