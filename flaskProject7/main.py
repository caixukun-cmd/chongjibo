import threading
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO
import datetime
import cv2
import logging
import os

from Video import Video
from danger_spy import danger_fall, set_danger
from detect_wave import detect_wave

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 存储所有视频流的字典
video_streams = {}

# 禁用其他日志
for logger_name in logging.root.manager.loggerDict:
    if logger_name != 'alert_logger':
        logging.getLogger(logger_name).disabled = True

# 创建一个专门用于警告的日志记录器
alert_logger = logging.getLogger('alert_logger')
alert_logger.setLevel(logging.WARNING)

# 添加文件处理器
file_handler = logging.FileHandler('alerts.log')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
alert_logger.addHandler(file_handler)


def log_alert(message):
    alert_logger.warning(message)


def process(stream_url, stream_id):
    cap = cv2.VideoCapture(stream_url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
    frame_skip = 5
    frame_count = 0

    while True:
        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        success, frame = cap.read()
        if not success:
            break
        if frame_count % frame_skip == 0:
            is_danger, fall_detected = danger_fall(frame, stream_id)
            wave_detected = detect_wave(frame)

            if fall_detected:
                message = f"Stream {stream_id}: 注意！有人摔倒"
                socketio.emit('exception_message', {'message': f"{time1} {message}"})
                log_alert(message)

            if wave_detected:
                message = f"Stream {stream_id}: 注意！挥手行为可疑！"
                socketio.emit('exception_message', {'message': f"{time1} {message}"})
                log_alert(message)

            if is_danger:
                message = f"Stream {stream_id}: 注意！有人进入危险区域！"
                socketio.emit('exception_message', {'message': f"{time1} {message}"})
                log_alert(message)

            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        frame_count += 1


@app.route('/video_feed/<stream_id>', methods=['GET'])
def video_feed(stream_id):
    global video_streams
    try:
        if stream_id not in video_streams:
            stream_url = f'rtmp://123.57.25.52:9090/live/{stream_id}'
            video_streams[stream_id] = process(stream_url, stream_id)

            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"video/{stream_id}_{timestamp}.mp4"
            save_thread = threading.Thread(target=Video, args=(stream_url, output_file))
            save_thread.start()

        return Response(video_streams[stream_id], mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        app.logger.error(f"Failed to stream video for ID {stream_id}: {str(e)}")
        return jsonify({'error': 'Failed to process video stream'}), 500


@app.route('/set_area', methods=['POST'])
def set_area():
    data = request.get_json()
    stream_id = 'stream_' + data.get('stream')
    x1 = data.get('x1')
    y1 = data.get('y1')
    x2 = data.get('x2')
    y2 = data.get('y2')

    # 为每个流单独设置危险区域
    set_danger(stream_id, int(x1), int(y1), int(x2), int(y2))

    return jsonify({'message': f'Area set for {stream_id}'}), 200


@app.route('/api/logs')
def get_logs():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))

    log_file_path = 'alerts.log'  # 日志文件路径

    if not os.path.exists(log_file_path):
        return jsonify({'error': 'Log file not found'}), 404

    with open(log_file_path, 'r') as file:
        all_logs = file.readlines()

    all_logs.reverse()  # 反转日志，使最新的日志在前面

    total_logs = len(all_logs)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    page_logs = all_logs[start_index:end_index]

    formatted_logs = []
    for log in page_logs:
        parts = log.strip().split(' - ', 1)
        if len(parts) == 2:
            timestamp, message = parts
            formatted_logs.append({
                'timestamp': timestamp,
                'message': message
            })

    return jsonify({
        'logs': formatted_logs,
        'total': total_logs
    })


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
