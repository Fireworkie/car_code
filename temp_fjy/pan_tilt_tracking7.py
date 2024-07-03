#-*- coding: UTF-8 -*-	
# 调用必需库
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pid import PID
import signal
import time
import sys
import cv2
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo

face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')


# 定义舵机
i2c_bus = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c_bus)
pwm.frequency = 50
servo_12 = servo.Servo(pwm.channels[12])
servo_15 = servo.Servo(pwm.channels[15])
servo_12.angle = 90
servo_15.angle = 90

# 键盘终止函数
def signal_handler(sig, frame):
    # 输出状态信息
	print("[INFO] You pressed `ctrl + c`! Exiting...")
	# 退出
	sys.exit()

def obj_center(faceX, faceY, centerX, centerY):
# 初始化摄像头
	cap = cv2.VideoCapture(0)

	while cap.isOpened():
    # 获取一帧图像
		ret, frame = cap.read()


    # 使用INTER_AREA插值法将图像的宽与高缩小为原来的一半
		frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		face_rects = face_cascade.detectMultiScale(gray, 1.3, minNeighbors=4, minSize=(75,75))

		for (x, y, w, h) in face_rects:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
			faceX.value = x + (w // 2)
			faceY.value = y + (h // 2)
			#print("Face detected at ({}, {})\n".format(faceX.value, faceY.value))
			#print("Center at ({}, {})\n".format(centerX, centerY))

		cv2.imshow('Face Detector', frame)

    # 按q键退出
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

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
		print("output_servoY: ", outputY.value)
		# 偏角变号
		#yaw = -1 * panAngle.value
		#pitch = -1 * tiltAngle.value
		if outputX.value > 5 and outputX.value < 175:
			servo_12.angle = outputX.value
		if outputY.value > 5 and outputY.value < 75:        
			servo_15.angle = max(5, min(75, outputY.value))+60
		
		# 设置舵机偏角

			

# 启动主程序
if __name__ == "__main__":
	servo_12.angle = 90
	servo_15.angle = 90
	# 启动多进程变量管理
	with Manager() as manager:
		# 舵机角度置零
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)
		faceX = manager.Value("i", 0)
		faceY = manager.Value("i", 0)
		outputX = manager.Value("i", 0)
		outputY = manager.Value("i", 0)

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
		# 4. setServos     - 根据PID控制的输出驱动舵机
		#                    
		processObjectCenter = Process(target=obj_center,args=(faceX, faceY, centerX, centerY))
		processPanning = Process(target=pidx_process,args=(panP, panI, panD, centerX, faceX, outputX))
		processTilting = Process(target=pidy_process,args=(tiltP, tiltI, tiltD, centerY, faceY, outputY))
		processSetServos = Process(target=set_servos, args=(outputX, outputY))

		# 开启4个进程
		processObjectCenter.start()
		processPanning.start()
		processTilting.start()
		processSetServos.start()

		# 添加4个进程
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processSetServos.join()

		# 关闭舵机
		#pan.detach()
		#.detach()
