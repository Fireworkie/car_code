import cv2
import socket
import numpy as np
from flask import Flask, Response
import json

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../temp_fjy/trainer/trainer.yml')
cap = cv2.VideoCapture(0)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
receiver_address=('localhost',8005)



def generate_frames():
        # 读取帧
    while True:
        ret, frame = cap.read()
        frame_show=frame
        if not ret:
            break
        # buffer=cv2.imencode('.jpg',frame)
        

        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # 在这里进行帧处理，例如图像识别、滤镜等
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # print(gray.shape.channels)
        # ch=gray.shape[2]
        # print(ch+"\n")
        frame_bytes=gray.tobytes() 
        # print(len(frame_bytes))
        sock.sendall(frame_bytes)

        # print(gray)
        # print("\n")
        face_rects = face_cascade.detectMultiScale(gray, 1.3, minNeighbors=4, minSize=(75,75))
        # print(face_rects)

        # rects_data=[]
        # for (x, y, w, h) in face_rects:
        #     rect={"x":x,"y":y,"w":w,"h":h}
        #     rects_data.append(rect)
        # json_data=json.dumps(rects_data)
        # sock.sendall(json_data.encode())
        # print(json_data)
        # print("\n")

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

    # 关闭连接



@app.route('/')
def index():
    return "OpenCV Camera Streaming with Flask"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    sock.connect(receiver_address)
    app.run(host='0.0.0.0', port=8003,debug=False)
