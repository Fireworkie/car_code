import cv2
from flask import Flask, Response

app = Flask(__name__)

# 打开摄像头
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # 读取帧
        ret, frame = cap.read()

        if not ret:
            break

        # 在这里进行帧处理，例如图像识别、滤镜等

        # 将处理后的帧转换为 JPEG 格式
        ret, buffer = cv2.imencode('.jpg', frame)

        # 将 JPEG 数据转换为字节流
        frame_bytes = buffer.tobytes()

        # 使用生成器输出帧的字节流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return "OpenCV Camera Streaming with Flask"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)
