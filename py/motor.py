import RPi.GPIO as GPIO
# import time
import json
import socket

cmd="stop"
class MotorDriver():
    def __init__(self, duty = 90, ENA = 33, IN1 = 35, IN2 = 37, ENB = 11, IN3 = 13, IN4 = 15, ENC = 22, IN5 = 24, IN6 = 26, END = 36, IN7 = 38, IN8 = 40):

        self.ENA = ENA
        self.IN1 = IN1
        self.IN2 = IN2

        self.ENB = ENB
        self.IN3 = IN3
        self.IN4 = IN4

        self.ENC = ENC
        self.IN5 = IN5
        self.IN6 = IN6

        self.END = END
        self.IN7 = IN7
        self.IN8 = IN8

        self.duty = duty

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        GPIO.setup(self.IN3,GPIO.OUT)
        GPIO.setup(self.IN4,GPIO.OUT)
        GPIO.setup(self.ENC, GPIO.OUT)
        GPIO.setup(self.IN5, GPIO.OUT)
        GPIO.setup(self.IN6, GPIO.OUT)
        GPIO.setup(self.END, GPIO.OUT)
        GPIO.setup(self.IN7, GPIO.OUT)
        GPIO.setup(self.IN8, GPIO.OUT)

        GPIO.output(self.ENA, 1)
        GPIO.output(self.ENB, 1)
        GPIO.output(self.ENC, 1)
        GPIO.output(self.END, 1)

        self.pwm1 = GPIO.PWM(self.ENA, 500)
        self.pwm2 = GPIO.PWM(self.ENB, 500)
        self.pwm3 = GPIO.PWM(self.ENC, 500)
        self.pwm4 = GPIO.PWM(self.END, 500)


        self.pwm1.start(duty)
        self.pwm2.start(duty)
        self.pwm3.start(duty)
        self.pwm4.start(duty)

    def forward(self):
            GPIO.output(self.IN1, 1)
            GPIO.output(self.IN2, 0)
            GPIO.output(self.IN3, 1)
            GPIO.output(self.IN4, 0)
            GPIO.output(self.IN5, 0)
            GPIO.output(self.IN6, 1)
            GPIO.output(self.IN7, 0)
            GPIO.output(self.IN8, 1)
    def back(self):
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 1)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 1)
            GPIO.output(self.IN5, 1)
            GPIO.output(self.IN6, 0)
            GPIO.output(self.IN7, 1)
            GPIO.output(self.IN8, 0)
    def right(self):
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 1)
            GPIO.output(self.IN3, 1)
            GPIO.output(self.IN4, 0)
            GPIO.output(self.IN5, 1)
            GPIO.output(self.IN6, 0)
            GPIO.output(self.IN7, 0)
            GPIO.output(self.IN8, 1)
    def left(self):
            GPIO.output(self.IN1, 1)
            GPIO.output(self.IN2, 0)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 1)
            GPIO.output(self.IN5, 0)
            GPIO.output(self.IN6, 1)
            GPIO.output(self.IN7, 1)
            GPIO.output(self.IN8, 0)
    def turn_left(self):
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 1)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 1)
            GPIO.output(self.IN5, 0)
            GPIO.output(self.IN6, 1)
            GPIO.output(self.IN7, 0)
            GPIO.output(self.IN8, 1)
    def turn_right(self):
            GPIO.output(self.IN1, 1)
            GPIO.output(self.IN2, 0)
            GPIO.output(self.IN3, 1)
            GPIO.output(self.IN4, 0)
            GPIO.output(self.IN5, 1)
            GPIO.output(self.IN6, 0)
            GPIO.output(self.IN7, 1)
            GPIO.output(self.IN8, 0)
    def stop(self):
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 0)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 0)
            GPIO.output(self.IN5, 0)
            GPIO.output(self.IN6, 0)
            GPIO.output(self.IN7, 0)
            GPIO.output(self.IN8, 0)
    def up(self):
        if self.duty <= 100:
            self.duty += 10
            self.pwm1.ChangeDutyCycle(self.duty)
            self.pwm2.ChangeDutyCycle(self.duty)
            self.pwm3.ChangeDutyCycle(self.duty)
            self.pwm4.ChangeDutyCycle(self.duty)
        else:
                print('get max')
    def down(self):
        if self.duty >= 0:
            self.duty -= 10
            self.pwm1.ChangeDutyCycle(self.duty)
            self.pwm2.ChangeDutyCycle(self.duty)
            self.pwm3.ChangeDutyCycle(self.duty)
            self.pwm4.ChangeDutyCycle(self.duty)
        else:
            print('get min')

def handle_client(client_socket):
    try:
        # 接收JSON数据
        json_data = client_socket.recv(1024).decode()
        print("接收到的JSON数据:", json_data)

        # 解析JSON数据
        parsed_data = json.loads(json_data)

        # 获取command字段的值
        global cmd 
        cmd = parsed_data.get('command')
        if cmd == "forward":
            motor.forward()
        if cmd == "backward":
            motor.back()
        if cmd == "left":
            motor.left()
        if cmd == "right":
            motor.right()
        if cmd == "turn_left":
            motor.turn_left()
        if cmd == "turn_right":
            motor.turn_right()
        if cmd == "stop":
            motor.stop()
        if cmd == "speedup":
            motor.up()
        if cmd == "speeddown":
            motor.down()
    except Exception as e:
        print("处理客户端数据时出现错误:", e)
    finally:
        # 关闭客户端连接
        client_socket.close()

def start_server():
    # 创建Socket对象
    global flag
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 绑定IP地址和端口号
        server_address = ('localhost', 8001)
        server_socket.bind(server_address)

        # 监听连接
        server_socket.listen(1)
        # print("服务器已启动，等待客户端连接...")
        global motor
        motor=MotorDriver()
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

start_server()
