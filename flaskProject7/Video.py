import cv2 as cv

def Video(stream_url, output_file):
    print(f"Starting to save video for stream: {stream_url} to file: {output_file}")
    cap = cv.VideoCapture(stream_url)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 180)

    if not cap.isOpened():
        print(f"Failed to open stream: {stream_url}")
        return

    # 获取实际的视频帧尺寸
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    size = (frame_width, frame_height)

    # 使用 'mp4v' 编码器来保存 MP4 文件
    # 将fourcc更改为h264格式
    fourcc = cv.VideoWriter_fourcc(*'avc1')
    out = cv.VideoWriter(output_file, fourcc, 20.0, size)


    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        out.write(frame)

    cap.release()
    out.release()
    print(f"Finished saving video for stream: {stream_url} to file: {output_file}")

# Example usage:
# Video('http://your_stream_url', 'output_file.mp4')
