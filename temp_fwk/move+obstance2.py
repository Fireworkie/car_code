import RPi.GPIO as GPIO
import threading
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

exitFlag = 0
duty = 70
ENA = 33
IN1 = 35
IN2 = 37
ENB = 11
IN3 = 13
IN4 = 15
ENC = 22
IN5 = 24
IN6 = 26
END = 36
IN7 = 38
IN8 = 40
trig = 16
echo = 18

GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)
GPIO.setup(ENC, GPIO.OUT)
GPIO.setup(IN5, GPIO.OUT)
GPIO.setup(IN6, GPIO.OUT)
GPIO.setup(END, GPIO.OUT)
GPIO.setup(IN7, GPIO.OUT)
GPIO.setup(IN8, GPIO.OUT)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.output(ENA, 1)
GPIO.output(ENB, 1)
GPIO.output(ENC, 1)
GPIO.output(END, 1)

pwm1 = GPIO.PWM(ENA, 500)
pwm2 = GPIO.PWM(ENB, 500)
pwm3 = GPIO.PWM(ENC, 500)
pwm4 = GPIO.PWM(END, 500)


pwm1.start(duty)
pwm2.start(duty)
pwm3.start(duty)
pwm4.start(duty)

  
def forward():
            GPIO.output(IN1, 1)
            GPIO.output(IN2, 0)
            GPIO.output(IN3, 1)
            GPIO.output(IN4, 0)
            GPIO.output(IN5, 0)
            GPIO.output(IN6, 1)
            GPIO.output(IN7, 0)
            GPIO.output(IN8, 1)
def back():
            GPIO.output(IN1, 0)
            GPIO.output(IN2, 1)
            GPIO.output(IN3, 0)
            GPIO.output(IN4, 1)
            GPIO.output(IN5, 1)
            GPIO.output(IN6, 0)
            GPIO.output(IN7, 1)
            GPIO.output(IN8, 0)
def right():
            GPIO.output(IN1, 1)
            GPIO.output(IN2, 0)
            GPIO.output(IN3, 0)
            GPIO.output(IN4, 1)
            GPIO.output(IN5, 1)
            GPIO.output(IN6, 0)
            GPIO.output(IN7, 0)
            GPIO.output(IN8, 1)
def left():
            GPIO.output(IN1, 0)
            GPIO.output(IN2, 1)
            GPIO.output(IN3, 1)
            GPIO.output(IN4, 0)
            GPIO.output(IN5, 0)
            GPIO.output(IN6, 1)
            GPIO.output(IN7, 1)
            GPIO.output(IN8, 0)
def stop():
            GPIO.output(IN1, 0)
            GPIO.output(IN2, 0)
            GPIO.output(IN3, 0)
            GPIO.output(IN4, 0)
            GPIO.output(IN5, 0)
            GPIO.output(IN6, 0)
            GPIO.output(IN7, 0)
            GPIO.output(IN8, 0)
def up():
        global duty
        if duty <= 200:
            duty += 10
            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(duty)
            pwm3.ChangeDutyCycle(duty)
            pwm4.ChangeDutyCycle(duty)
        else:
                print('get max')
def down():
        global duty
        if duty >= 0:
            duty -= 10
            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(duty)
            pwm3.ChangeDutyCycle(duty)
            pwm4.ChangeDutyCycle(duty)
        else:
            print('get min')

def get_distance():
    """返回到障碍物的距离"""
    # 向trig端发送10us高电平信号
    GPIO.output(trig, 1)
    time.sleep(0.00001)
    # 结束发送
    GPIO.output(trig, 0)
    # 通过echo端开始检测回声信号
    while GPIO.input(echo) == 0:
        # 获取检测回响信号的开始时间
        start_time = time.time()
    while GPIO.input(echo) == 1:
        # 获取检测到回响的时间
        end_time = time.time()
    # 计算超声波从发送到返回的时长
    duration = end_time - start_time
    # 计算距离，单位为cm
    distance = duration * (34000)/2
    return distance

def move():
    try:
        while True:
            cmd = input("输入w(forward) or s(back) or a(left) or d(right) or q(up) or z(down)or x(stop): ")
            if cmd == "w":
                forward()
            if cmd == "s":
                back()
            if cmd == "a":
                left()
            if cmd == "d":
                right()
            if cmd == "x":
                stop()
            if cmd == "q":
                up()
            if cmd == "z":
                down()
    except KeyboardInterrupt: #用户输入中断键（Ctrl + C），退出
        GPIO.cleanup()

def obstance():
    try:
        GPIO.output(IN1, 1)
        GPIO.output(IN2, 0)
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 1)
        GPIO.output(IN5, 0)
        GPIO.output(IN6, 1)
        GPIO.output(IN7, 1)
        GPIO.output(IN8, 0)
        time.sleep(2)
        GPIO.output(IN8, 0)
        GPIO.output(IN1, 0)
        GPIO.output(IN2, 0)
        GPIO.output(IN3, 0)
        GPIO.output(IN4, 0)
        GPIO.output(IN5, 0)
        GPIO.output(IN6, 0)
        GPIO.output(IN7, 0)
        time.sleep(1)
    except:
         print("111")


if __name__ == "__main__":
    try:
        thread1 = threading.Thread(target=obstance)
        thread2 = threading.Thread(target=move)
        while True:
            thread2.start()
            distance = get_distance()
            print("Distance: {:.2f}cm".format(distance))
            # 如果距离小于20cm，则执行相应的避障操作
            if distance < 20:
                thread1.join()
                thread2.join()
    except:
        print ("Error: unable to start thread")