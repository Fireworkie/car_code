#-*- coding: UTF-8 -*-	
# 调用必需库
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from objcenter import ObjCenter
from pid import PID
import signal
import time
import sys
import cv2
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo

cascade_path = '/home/fireworkie/car/Python/cascades/haarcascade_frontalface_default.xml'


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
	pwm.setPWM(12, 0, 0)
	pwm.setPWM(15, 0, 0)

	# 关闭舵机
	#pan.detach()
	#tilt.detach()
  
	# 退出
	sys.exit()

def obj_center(cascade_path,objX, objY, centerX, centerY):
	# ctrl+c退出进程
	signal.signal(signal.SIGINT, signal_handler)
	# 启动视频流并缓冲
	#vs = VideoStream(usePiCamera=True).start()
	#vs = VideoStream(src=0).start()
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 80)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 60)
	time.sleep(2.0)

	# 初始化人脸中心探测器
	obj = ObjCenter(cascade_path)
	# 进入循环
	while True:
		# 读取视频流
		print("准备读取视频流")
		ret, frame = cap.read()  # 注意这里返回了两个值  
		if not ret:
			print("无帧")
		#frame = cv2.resize(frame, (80, 60))
		print("读取视频流完成")
		# 显示图像
		cv2.imshow("frame", frame)

		# 找到图像中心
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		# 找到人脸中心
		objectLoc = obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect) = objectLoc

		# 绘制人脸外界矩形
		if rect is not None:
			(x, y, w, h) = rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

			# 显示图像
			#cv2.imshow("Pan-Tilt Face Tracking", frame)

def pid_process(output, p, i, d, objCoord, centerCoord):
	# ctrl+c退出进程
	signal.signal(signal.SIGINT, signal_handler)
	
 	# 创建一个PID类的对象并初始化
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# 进入循环
	while True:
		# 计算误差
		error = centerCoord.value - objCoord.value

		# 更新输出值
		output.value = p.update(error)
		print("output: ", output.value)

def set_servos(panAngle, tiltAngle):
	# ctrl+c退出进程
	signal.signal(signal.SIGINT, signal_handler)
	servo_12.angle = 90
	servo_15.angle = 90
	# 进入循环
	while True:
		# 偏角变号
		#yaw = -1 * panAngle.value
		#pitch = -1 * tiltAngle.value
		if panAngle.value > 5 and panAngle.value < 175:
			servo_12.angle = panAngle.value
		if tiltAngle.value > 65 and tiltAngle.value < 135:		
			servo_15.angle = tiltAngle.value
		# 设置舵机偏角

			

# 启动主程序
if __name__ == "__main__":
	servo_12.angle = 90
	servo_15.angle = 90
	# 启动多进程变量管理
	with Manager() as manager:
		# 舵机角度置零
		servo_12.angle = 90
		servo_15.angle = 90
		# 为图像中心坐标赋初值
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)

		# 为人脸中心坐标赋初值
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

	    # panAngle和tiltAngle分别是两个舵机的PID控制输出量	    
		panAngle = manager.Value("i", 0)
		tiltAngle = manager.Value("i", 0)

		# 设置一级舵机的PID参数
		panP = manager.Value("f", 0.2)
		panI = manager.Value("f", 0.04)
		panD = manager.Value("f", 0.008)

		# 设置二级舵机的PID参数
		tiltP = manager.Value("f", 0.22)
		tiltI = manager.Value("f", 0.05)
		tiltD = manager.Value("f", 0.008)

    	# 创建4个独立进程
        # 1. objectCenter  - 探测人脸
		# 2. panning       - 对一级舵机进行PID控制，控制偏航角
		# 3. tilting       - 对二级舵机进行PID控制，控制俯仰角
		# 4. setServos     - 根据PID控制的输出驱动舵机
		#                    
		processObjectCenter = Process(target=obj_center,args=(cascade_path,objX, objY, centerX, centerY))
		processPanning = Process(target=pid_process,args=(panAngle, panP, panI, panD, objX, centerX))
		processTilting = Process(target=pid_process,args=(tiltAngle, tiltP, tiltI, tiltD, objY, centerY))
		processSetServos = Process(target=set_servos, args=(panAngle, tiltAngle))

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
		pwm.setPWM(12, 0, 0)
		pwm.setPWM(15, 0, 0)
