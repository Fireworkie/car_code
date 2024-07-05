#-*- coding: UTF-8 -*-	
# 调用必需库
# import os
import cv2
import sys
import json
# import time
import numpy as np
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
# import json

lock = threading.Lock()
app = Flask(__name__)
face_list = list(["0",0,0,320,240]*10)
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../temp_fjy/trainer/trainer.yml')
# 定义舵机
i2c_bus = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c_bus)
pwm.frequency = 50
servo_12 = servo.Servo(pwm.channels[12])
servo_15 = servo.Servo(pwm.channels[15])
servo_12.angle = 90
servo_15.angle = 90
# cap = cv2.VideoCapture(0)

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
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定IP地址和端口号
	server_address = ('localhost', 8005)
	server_socket.bind(server_address)

        # 监听连接
	server_socket.listen(1)

	while True:
		# ret, frame = cap.read()
		client_socket, client_address = server_socket.accept()
		print("客户端已连接:", client_address)

		while True:
			frame_bytes_all = b''
			while(frame_bytes_all.__len__() != 76800):
				frame_bytes = client_socket.recv(76800)
				frame_bytes_all += frame_bytes
				continue
			frame=np.frombuffer(frame_bytes_all, dtype=np.uint8).squeeze().reshape(240,320)
			# print(frame)
			# print("\n")
			# print("success\n")
			face_rects = face_cascade.detectMultiScale(frame, 1.3, minNeighbors=4, minSize=(75,75))
			print(face_rects)
			print("\n")
			global faceX, faceY
			for (x, y, w, h) in face_rects:
				if len(face_rects) == 0:
					continue
				else:
					with lock:
						faceX= x + w//2
						faceY = y + h//2					




			# 	# print("num:"+i+"\n")
			# 	roi = cv2.resize(frame[y:y+h, x:x+w], (92, 112))
			# 	id, confidence = recognizer.predict(roi)
			# 	id_str = str(id)
			# 	with lock:
			# 		face_list[i] = (id_str[0], x, y, w, h)

		# print("客户端连接断开:", client_address)

			# frame_bytes_all =client_socket.recv(76800)

			# print(frame_bytes+"\n")
			# if frame_bytes == b'':
			# if len(frame_bytes) == 0:
			# 	print("No data received\n")
			# 	continue
			
			# frame=np.squeeze(frame)

			# 	continue
			# print(frame_bytes+"\n")
			# if frame_bytes.endswith(b'\xff\xd9'):

			# ret,frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
			# if ret == False :
				# print("decode failed\n")
			# 	continue
		# ret, buffer = cv2.imencode('.jpg', frame)
        # # 将 JPEG 数据转换为字节流
		# frame_bytes = buffer.tobytes()
		# client_socket.sendall(frame_bytes)
			# print("success\n")
		# if not ret:
		# 	break
			# frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # 在这里进行帧处理，例如图像识别、滤镜等
			# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# print("success\n")
			# global face_r
			# face_rects = face_cascade.detectMultiScale(frame, 1.3, minNeighbors=4, minSize=(75,75))
			# print("face_rects: ", face_rects)
			# data_rec=client_socket.recv(1024)

			# json_data = data_rec.decode()
			# print("接收到的JSON数据:", json_data)
			# rects_data = json.loads(json_data)
			# face_rects = []
			# for rect in rects_data:
			# 	x=rect["x"]
			# 	y=rect["y"]
			# 	w=rect["w"]
			# 	h=rect["h"]
			# 	face_rects.append((x,y,w,h))

			# for i, (x, y, w, h) in enumerate(face_rects):
			# 	print("num:"+i+"\n")
			# 	roi = cv2.resize(frame[y:y+h, x:x+w], (92, 112))
			# 	id, confidence = recognizer.predict(roi)
			# 	id_str = str(id)
			# 	with lock:
			# 		face_list[i] = (id_str[0], x, y, w, h)

			
			# confidence = "{0}%".format(round(100 - confidence))
			#cv2.putText(frame_show, "person: " + str(id_str[0]), (vx+5, vy-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#			cv2.putText(frame_show, "Confidence: " + str(confidence), (vx+5, vy+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


        # 使用生成器输出帧的字节流
#		yield ( b'--frame\r\n'
#				b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
		
	# client_socket.close()
	# server_socket.close()
	# cap.release()	


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

#@app.route('/')
#def index():
#    return "OpenCV Camera Streaming with Flask"

#@app.route('/video_feed')
#def video_feed():
#    return Response(face_reco(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 启动主程序
if __name__ == "__main__":
	

                
		
		# processObjectCenter = Process(target=face_reco,args=(face_list,))
	# print("ready")
	processObjectCenter = threading.Thread(target=face_reco)
	#processChoose = threading.Thread(target=start_server)
	processPanning = threading.Thread(target=pidx_process,args=(panP, panI, panD))
	processTilting = threading.Thread(target=pidy_process,args=(tiltP, tiltI, tiltD))
	processSetServos = threading.Thread(target=set_servos)

		# 开启5个进程
	processObjectCenter.start()
	#processChoose.start()
	processPanning.start()
	processTilting.start()
	processSetServos.start()
	# app.run(host='0.0.0.0', port=8003,debug=False)
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