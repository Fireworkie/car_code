import RPi.GPIO as GPIO
import time

class MotorDriver():
    def __init__(self, duty = 70, ENA = 33, IN1 = 35, IN2 = 37, ENB = 11, IN3 = 13, IN4 = 15, ENC = 22, IN5 = 24, IN6 = 26, END = 36, IN7 = 38, IN8 = 40):

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
            GPIO.output(self.IN1, 1)
            GPIO.output(self.IN2, 0)
            GPIO.output(self.IN3, 0)
            GPIO.output(self.IN4, 1)
            GPIO.output(self.IN5, 1)
            GPIO.output(self.IN6, 0)
            GPIO.output(self.IN7, 0)
            GPIO.output(self.IN8, 1)
    def left(self):
            GPIO.output(self.IN1, 0)
            GPIO.output(self.IN2, 1)
            GPIO.output(self.IN3, 1)
            GPIO.output(self.IN4, 0)
            GPIO.output(self.IN5, 0)
            GPIO.output(self.IN6, 1)
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
        if self.duty <= 200:
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
if __name__ == "__main__":
    motor = MotorDriver()
    try:
        while True:
            cmd = input("输入w(forward) or s(back) or a(left) or d(right) or q(up) or z(down)or x(stop): ")
            if cmd == "w":
                motor.forward()
            if cmd == "s":
                motor.back()
            if cmd == "a":
                motor.left()
            if cmd == "d":
                motor.right()
            if cmd == "x":
                motor.stop()
            if cmd == "q":
                motor.up()
            if cmd == "z":
                motor.down()
    except KeyboardInterrupt: #用户输入中断键（Ctrl + C），退出
        GPIO.cleanup()