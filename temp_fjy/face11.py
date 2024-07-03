#-*- coding: UTF-8 -*-	
# 调用必需库
# import os
import cv2
import sys
import json
# import time
import busio
import socket
# import signal
from pid import PID
from board import SCL, SDA
from adafruit_motor import servo
from flask import Flask, Response
# from multiprocessing import Manager
from adafruit_pca9685 import PCA9685
# from imutils.video import VideoStream
# from multiprocessing import Process, Queue
import threading

lock = threading.Lock()
app = Flask(__name__)
face_list = list()
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
# 定义舵机
i2c_bus = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c_bus)
pwm.frequency = 50
servo_12 = servo.Servo(pwm.channels[12])
servo_15 = servo.Servo(pwm.channels[15])
servo_12.angle = 90
servo_15.angle = 90
cap = cv2.VideoCapture(0)

faceX = 0
faceY = 0
outputX = 0
outputY = 0
# choose = 0

		# 设置一级舵机的PID参数
panP = 0.0769
panI = 0.03
panD = 0.00415

		# 设置二级舵机的PID参数
tiltP = 0.0768
tiltI = 0.03
tiltD = 0.00415
def start_server():
    # 创建Socket对象
	global face_list
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
        # 绑定IP地址和端口号
		server_address = ('localhost', 8004)
		server_socket.bind(server_address)

        # 监听连接
		server_socket.listen(1)
        # print("服务器已启动，等待客户端连接...")
        # 接受连接
		while True:
			client_socket, client_address = server_socket.accept()
			print("客户端已连接:", client_address)
        # 处理客户端数据
#            handle_client(client_socket)
			try:
        # 接收JSON数据
				json_data = client_socket.recv(1024).decode()
				print("接收到的JSON数据:", json_data)
        	# 解析JSON数据
				parsed_data = json.loads(json_data)
        	# 获取command字段的值
				global  faceX, faceY
				choose = parsed_data.get('traceid')
				for i in range(len(face_list)):
					(ii, x, y, w, h) = face_list[i]
					if ii == choose:
						with lock:
							faceX= x + w//2
							faceY = y + h//2 
			except Exception as e:
				print("处理客户端数据时出现错误:", e)
			finally:
        	# 关闭客户端连接
				client_socket.close()
	except Exception as e:
		print("服务器运行时出现错误:", e)
	finally:
        # 关闭服务器
		server_socket.close()
		
def face_reco():
	# signal.signal(signal.SIGINT, signal_handler)
	global face_list
	while True:
		ret, frame = cap.read()
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
			with lock:
				face_list[i] = (id_str[0], x, y, w, h)
			# confidence = "{0}%".format(round(100 - confidence))
			cv2.putText(frame_show, "person: " + str(id_str[0]), (vx+5, vy-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#			cv2.putText(frame_show, "Confidence: " + str(confidence), (vx+5, vy+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

		ret, buffer = cv2.imencode('.jpg', frame_show)

        # 将 JPEG 数据转换为字节流
		frame_bytes = buffer.tobytes()

        # 使用生成器输出帧的字节流
		yield ( b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def pidx_process(p, i, d):
	# ctrl+c退出进程
	# signal.signal(signal.SIGINT, signal_handler)
	
 	# 创建一个PID类的对象并初始化
	p = PID(p, i, d)
	p.initialize()
	global faceX
	# 进入循环
	while True:
		# 计算误差
		error = 480 - faceX
		#print("centerX: \n", centerX.value)
		#print("faceX: \n", faceX.value)
		#print("error: \n", error)
		global outputX
		# 更新输出值
		with lock:
			outputX = p.update(error)
		#print("outputX: \n", outputX.value)
		#time.sleep(0.25)

def pidy_process(p,i,d):
	# ctrl+c退出进程
	# signal.signal(signal.SIGINT, signal_handler)
	
 	# 创建一个PID类的对象并初始化
	p = PID(p, i, d)
	p.initialize()
	global faceY
	# 进入循环
	while True:
		# 计算误差
		error = 320 - faceY
		#print("centerY: \n", centerY.value)
		#print("faceY: \n", faceY.value)
		#print("error: \n", error)
		global outputY
		# 更新输出值'
		with lock:
			outputY= p.update(error)
		#print("outputY: \n", outputY.value)
		#time.sleep(0.25)

def set_servos():
	# ctrl+c退出进程
	# signal.signal(signal.SIGINT, signal_handler)
	global outputX, outputY
	servo_12.angle = 90
	servo_15.angle = 90
	# 进入循环
	while True:
		#print("output_servoX: ", outputX.value)
		#print("output_servoY: ", outputY.value)
		# 偏角变号
		#yaw = -1 * panAngle.value
		#pitch = -1 * tiltAngle.value
		if outputX > 5 and outputX < 175:
			servo_12.angle = outputX
		if outputY > 5 and outputY < 75:        
			servo_15.angle = max(5, min(75, outputY))+60
		
		# 设置舵机偏角

@app.route('/')
def index():
    return "OpenCV Camera Streaming with Flask"

@app.route('/video_feed')
def video_feed():
    return Response(face_reco(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 启动主程序
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8003,debug=False)
	
	# signal.signal(signal.SIGINT, signal_handler)
	# 启动多进程变量管理
		# 舵机角度置零
	

    	# 创建4个独立进程
        # 1. objectCenter  - 探测人脸
		# 2. panning       - 对一级舵机进行PID控制，控制偏航角
		# 3. tilting       - 对二级舵机进行PID控制，控制俯仰角
		# 4. setServos     - 根据PID控制的输出驱动舵机s
                
		
		# processObjectCenter = Process(target=face_reco,args=(face_list,))

	processChoose = threading.Thread(target=start_server,args=())
	processPanning = threading.Thread(target=pidx_process,args=(panP, panI, panD))
	processTilting = threading.Thread(target=pidy_process,args=(tiltP, tiltI, tiltD))
	processSetServos = threading.Thread(target=set_servos, args=())

		# 开启5个进程
		# processObjectCenter.start()
	processChoose.start()
	processPanning.start()
	processTilting.start()
	processSetServos.start()

#		processObjectCenter.join()
#		processChoose.join()
#		processPanning.join()
#		processTilting.join()
#		processSetServos.join()

		# 关闭舵机
		#pan.detach()
		#.detach()

#迭代淘汰函数		
#def number_judge(id_str,i,roi):  #传照片和数字的
#	if id_str[0] == i:
#				#发送数字和截取一帧图片给前端
#		ret, buffer = cv2.imencode('.jpg', roi)
#		frame_bytes = buffer.tobytes()
#		yield (b'--frame\r\n'
#				b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#		yield (b'--data\r\n'
#				b'Content-Type: text/plain\r\n\r\n' + str(i).encode() + b'\r\n')

#需要解决一个问题：只需要传一次照片，判断数字即可，不需要多次传送照片（可能要写两个函数）
#def obj_center(faceX, faceY, centerX, centerY,face_rects,frame): #想让他只返回四个值
    # 使用INTER_AREA插值法将图像的宽与高缩小为原来的一半
#		frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
#		(H, W) = frame.shape[:2]
#		centerX.value = W // 2
#		centerY.value = H // 2
#		for (x, y, w, h) in face_rects:
#			faceX.value = x + (w // 2)
#			faceY.value = y + (h // 2)
		 #  #需要解决一个问题：只需要传一次照片，判断数字即可，不需要多次传送照片（可能要写两个函数）

			#print("Face detected at ({}, {})\n".format(faceX.value, faceY.value))
			#print("Center at ({}, {})\n".format(centerX, centerY))