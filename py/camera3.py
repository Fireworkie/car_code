import cv2
import socket
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../temp_fjy/trainer/trainer.yml')
# 打开摄像头
#cap = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_address = ('localhost', 8005)  # 接收程序的主机和端口
sock.bind(receiver_address)
print('等待连接...')    
sock.listen(1)

def generate_frames():
    # signal.signal(signal.SIGINT, signal_handler)
    while True:
        conn, addr = sock.accept()
        print('连接已建立:', addr)
        frame_bytes = b''
#    while True:
        data = conn.recv(4096)
        if not data:
            break
        frame_bytes += data

    # 将接收到的字节流转换为图像
#        buffer = pickle.loads(frame_bytes)
#        frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        # 读取帧
#        ret, frame = cap.read()
        frame_show=frame

        if not ret:
            break
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # 在这里进行帧处理，例如图像识别、滤镜等
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, minNeighbors=4, minSize=(75,75))

        for i, (x, y, w, h) in enumerate(face_rects):
            vx=x*2
            vy=y*2
            vw=w*2
            vh=h*2
            cv2.rectangle(frame_show, (vx, vy), (vx+vw, vy+vh), (255, 0, 0), 2)

            roi = cv2.resize(gray[y:y+h, x:x+w], (92, 112))
            id, confidence = recognizer.predict(roi)
            id_str = str(id)
            # face_list[i] = (id_str[0], x, y, w, h)

            confidence = "{0}%".format(round(100 - confidence))
            cv2.putText(frame_show, "person: " + str(id_str[0]), (vx+5, vy-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#            cv2.putText(frame_show, "Confidence: " + str(confidence), (vx+5, vy+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 将处理后的帧转换为 JPEG 格式
        ret, buffer = cv2.imencode('.jpg', frame_show)

        # 将 JPEG 数据转换为字节流
        frame_bytes = buffer.tobytes()

        # 使用生成器输出帧的字节流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        conn.close()
    # 关闭连接
@app.route('/')
def index():
    return "OpenCV Camera Streaming with Flask"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003,debug=False)
