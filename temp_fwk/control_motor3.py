import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo
i2c_bus = busio.I2C(SCL, SDA)
# 使用默认地址初始化PWM设备
pwm = PCA9685(i2c_bus)
# 将频率设置为50 Hz
pwm.frequency = 50
# 指定第12通道的舵机（从0开始）
servo_12 = servo.Servo(pwm.channels[12])
# 指定第15通道的舵机
servo_15 = servo.Servo(pwm.channels[15])
print('Moving servo on channel 0, press Ctrl-C to quit...')
servo_12.angle = 0
servo_15.angle = 0
while True:
    x = input('x is(0-180): ')
    y = input('y is(0-180): ')
    servo_12.angle = int(x)
    servo_15.angle = int(y)
    time.sleep(1)
