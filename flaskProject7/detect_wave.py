import time

import cv2
import mediapipe as mp
import collections

# 初始化 MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 用于存储手部位置的历史记录
hand_positions = collections.deque(maxlen=10)  # 存储最近10帧的手部位置

last_wave_time = 0


def can_emit():
    global last_wave_time
    current_time = time.time()
    if current_time - last_wave_time >= 5:
        last_wave_time = current_time
        return True
    return False


def detect_wave(frame):
    wave_detected = False
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 可视化手部关键点
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 记录手部关键点的x和y坐标
            x_coords = [landmark.x * frame.shape[1] for landmark in hand_landmarks.landmark]
            y_coords = [landmark.y * frame.shape[0] for landmark in hand_landmarks.landmark]

            # 将当前手部位置添加到历史记录中
            hand_positions.append((x_coords, y_coords))

            # 检测手部位置变化
            if len(hand_positions) >= 10:  # 确保有足够的历史记录进行检测
                x_min = min([min(pos[0]) for pos in hand_positions])
                x_max = max([max(pos[0]) for pos in hand_positions])
                y_min = min([min(pos[1]) for pos in hand_positions])
                y_max = max([max(pos[1]) for pos in hand_positions])

                if (x_max - x_min) > 30 or (y_max - y_min) > 30:  # 根据实际情况调整阈值
                    color = (0, 255, 0)  # 绿色标记挥手
                    label = "WAVE DETECTED"
                    cv2.putText(frame, label, (int(x_coords[0]), int(y_coords[0]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    if can_emit():
                        wave_detected=True
                else:
                    wave_detected = False

    return wave_detected
