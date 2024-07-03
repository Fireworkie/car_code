#-*- coding: UTF-8 -*-	
# 调用必需库
from multiprocessing import Manager
from multiprocessing import Process, Queue
from imutils.video import VideoStream
from pid import PID
import signal
import time
import sys
import cv2
import os
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo
import cv2
from flask import Flask, Response

app = Flask(__name__)

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
def face_reco(face_list):
	signal.signal(signal.SIGINT, signal_handler)
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
			face_list[i] = (id_str[0], x, y, w, h)

			confidence = "{0}%".format(round(100 - confidence))
			cv2.putText(frame_show, "person: " + str(id_str[0]), (vx+5, vy-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
			cv2.putText(frame_show, "Confidence: " + str(confidence), (vx+5, vy+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

		ret, buffer = cv2.imencode('.jpg', frame_show)

        # 将 JPEG 数据转换为字节流
		frame_bytes = buffer.tobytes()

        # 使用生成器输出帧的字节流
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def choose_detect(input_queue, face_list, choose, faceX, faceY):
	signal.signal(signal.SIGINT, signal_handler)
	while True:
		i = 0
		for i in range(len(face_list)):
			(ii, x, y, w, h) = face_list[i].value
			if not input_queue.empty():
				choose = input_queue.get()
				#print(f"选择了要追踪的人脸：{choose}")
			if ii == choose:
				faceX.value = x + w//2
				faceY.value = y + h//2 

# 键盘终止函数
def signal_handler(sig, frame):
    # 输出状态信息
	print("[INFO] You pressed `ctrl + c`! Exiting...")
	cap.release()
    
    # 停止所有舵机
	#for channel in range(16):  # PCA9685有16个通道
	#	pwm.set_pwm(channel, 0, 0)
    
    # 其他必要的清理工作
	print("Cleanup complete.")
	# 退出
	sys.exit()

def number_judge(id_str,i,roi):  #传照片和数字的
	if id_str[0] == i:
				#发送数字和截取一帧图片给前端
		ret, buffer = cv2.imencode('.jpg', roi)
		frame_bytes = buffer.tobytes()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
		yield (b'--data\r\n'
				b'Content-Type: text/plain\r\n\r\n' + str(i).encode() + b'\r\n')

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


def pidx_process(p, i, d, centerX, faceX, outputX):
	# ctrl+c退出进程
	signal.signal(signal.SIGINT, signal_handler)
	
 	# 创建一个PID类的对象并初始化
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# 进入循环
	while True:
		# 计算误差
		error = 480 - faceX.value
		#print("centerX: \n", centerX.value)
		#print("faceX: \n", faceX.value)
		#print("error: \n", error)

		# 更新输出值
		outputX.value = p.update(error)
		#print("outputX: \n", outputX.value)
		#time.sleep(0.25)

def pidy_process(p, i, d, centerY, faceY, outputY):
	# ctrl+c退出进程
	signal.signal(signal.SIGINT, signal_handler)
	
 	# 创建一个PID类的对象并初始化
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# 进入循环
	while True:
		# 计算误差
		error = 320 - faceY.value
		#print("centerY: \n", centerY.value)
		#print("faceY: \n", faceY.value)
		#print("error: \n", error)

		# 更新输出值
		outputY.value = p.update(error)
		#print("outputY: \n", outputY.value)
		#time.sleep(0.25)

def set_servos(outputX, outputY):
	# ctrl+c退出进程
	signal.signal(signal.SIGINT, signal_handler)
	servo_12.angle = 90
	servo_15.angle = 90
	# 进入循环
	while True:
		#print("output_servoX: ", outputX.value)
		#print("output_servoY: ", outputY.value)
		# 偏角变号
		#yaw = -1 * panAngle.value
		#pitch = -1 * tiltAngle.value
		if outputX.value > 5 and outputX.value < 175:
			servo_12.angle = outputX.value
		if outputY.value > 5 and outputY.value < 75:        
			servo_15.angle = max(5, min(75, outputY.value))+60
		
		# 设置舵机偏角

@app.route('/')
def index():
    return "OpenCV Camera Streaming with Flask"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 启动主程序
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8003,debug=False)
	
	servo_12.angle = 90
	servo_15.angle = 90

	input_queue = Queue()
	# 启动多进程变量管理
	with Manager() as manager:
		# 舵机角度置零
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)
		faceX = manager.Value("i", 0)
		faceY = manager.Value("i", 0)
		outputX = manager.Value("i", 0)
		outputY = manager.Value("i", 0)
		face_list = manager.list()
		choose = manager.Value("i", 0)

		# 设置一级舵机的PID参数
		panP = manager.Value("f", 0.0769)
		panI = manager.Value("f", 0.03)
		panD = manager.Value("f", 0.00415)

		# 设置二级舵机的PID参数
		tiltP = manager.Value("f", 0.0768)
		tiltI = manager.Value("f", 0.03)
		tiltD = manager.Value("f", 0.00415)

    	# 创建4个独立进程
        # 1. objectCenter  - 探测人脸
		# 2. panning       - 对一级舵机进行PID控制，控制偏航角
		# 3. tilting       - 对二级舵机进行PID控制，控制俯仰角
		# 4. setServos     - 根据PID控制的输出驱动舵机s
		#                    
		processObjectCenter = Process(target=face_reco,args=(face_list,))
		processChoose = Process(target=choose_detect,args=(input_queue, face_list, choose, faceX, faceY))

		processPanning = Process(target=pidx_process,args=(panP, panI, panD, centerX, faceX, outputX))
		processTilting = Process(target=pidy_process,args=(tiltP, tiltI, tiltD, centerY, faceY, outputY))
		processSetServos = Process(target=set_servos, args=(outputX, outputY))

		# 开启5个进程
		processObjectCenter.start()
		processChoose.start()
		processPanning.start()
		processTilting.start()
		processSetServos.start()

		try:
			while True:
				choice = input('选择要追踪的人脸：')
				input_queue.put(choice)
		except KeyboardInterrupt:
			print("\n程序被用户中断。")

#		processObjectCenter.join()
#		processChoose.join()
#		processPanning.join()
#		processTilting.join()
#		processSetServos.join()

		# 关闭舵机
		#pan.detach()
		#.detach()
