import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo
import socket
import json
import threading

i2c_bus = busio.I2C(SCL, SDA)
# 使用默认地址初始化PWM设备
pwm = PCA9685(i2c_bus)
# 将频率设置为50 Hz
pwm.frequency = 50
# 指定第12通道的舵机（从0开始）
servo_12 = servo.Servo(pwm.channels[12])
# 指定第15通道的舵机
servo_15 = servo.Servo(pwm.channels[15])
servo_12.angle = 90
#x
servo_15.angle = 90
#y
# 全局变量，用于控制伺服电机转动状态
vx = 0
vy = 0

lock = threading.Lock()

# 伺服电机控制线程
def motor_controlX_thread():
    global vx
    while True:
        with lock:
            if vx==1:
                servo_12.angle=min(servo_12.angle+1,180)
            if vx==-1:
                servo_12.angle=max(servo_12.angle-1,0)
        time.sleep(0.01)

def motor_controlY_thread():
    global vy
    while True:
        with lock:
            if vy==1:
                servo_15.angle=min(servo_15.angle+1,135)
            if vy==-1:
                servo_15.angle=max(servo_15.angle-1,65)
        time.sleep(0.01)


# 监听端口线程
def handle_client(client_socket):
    try:
        # 接收客户端数据
        json_data = client_socket.recv(1024)
        print("接收到客户端数据:", json_data.decode())
        parsed_data = json.loads(json_data)
        global vx, vy
        if(parsed_data.get("xy")=="x"):
            with lock:
                vx=int(parsed_data.get("data"))

        if(parsed_data.get("xy")=="y"):
            with lock:
                vy=int(parsed_data.get("data"))
        if(parsed_data.get("xy")=="stop"):
            with lock:
                vx=0
                vy=0
    except Exception as e:
        print("解析客户端数据时出现错误:", e)
    finally:
        # 关闭客户端连接
        client_socket.close()

def start_server():
    # 创建Socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 绑定IP地址和端口号
        server_address = ('localhost', 8002)
        server_socket.bind(server_address)
        # 监听连接
        server_socket.listen(1)
        # print("服务器已启动，等待客户端连接...")
        # 接受连接
        while True:
            client_socket, client_address = server_socket.accept()
            print("客户端已连接:", client_address)
        # 处理客户端数据
            handle_client(client_socket)
    except Exception as e:
        print("服务器运行时出现错误:", e)
    finally:
        # 关闭服务器
        server_socket.close()

# 创建并启动线程
motorX_thread = threading.Thread(target=motor_controlX_thread)
motorY_thread = threading.Thread(target=motor_controlY_thread)
listen_thread = threading.Thread(target=start_server)
motorX_thread.start()
motorY_thread.start()
listen_thread.start()