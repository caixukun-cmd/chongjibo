import cv2
import numpy as np
from face_recognition import detector, sp, facerec, registered_faces

# 假设每个人脸的宽度在现实生活中是14.0 cm，这个参数可以根据实际情况调整
KNOWN_FACE_WIDTH = 14.0
# 焦距参数，需要根据摄像机实际情况校准
FOCAL_LENGTH = 500

def face(frame, alert_threshold=50):
    # 1. 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 2. 检测人脸
    faces = detector(gray, 1)
    for face in faces:
        # 获取人脸关键点
        shape = sp(frame, face)
        # 计算人脸的128维编码
        face_encoding = np.array(facerec.compute_face_descriptor(frame, shape))
        # 比较捕获的人脸与已注册人脸库中的编码，以判断是否为已知人脸
        color = (0, 255, 0)  # 绿色标记已注册人脸
        # 在人脸周围绘制矩形框
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), color, 2)

        # 计算人脸宽度并估算距离
        face_width_in_frame = face.right() - face.left()
        distance = (KNOWN_FACE_WIDTH * FOCAL_LENGTH) / face_width_in_frame

        # 添加文本标签
        label = f"{distance:.2f} cm"
        cv2.putText(frame, label, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 告警
        if distance < alert_threshold:
            alert(frame)

def alert(frame):
    # 在帧上添加红色告警标记
    height, width, _ = frame.shape
    cv2.putText(frame, 'ALERT: Too Close!', (width//2 - 100, height//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
