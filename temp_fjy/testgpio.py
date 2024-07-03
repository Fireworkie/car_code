from gpiozero import AngularServo  
from time import sleep 
  
# 创建一个AngularServo对象，连接到GPIO 17引脚，设置角度范围为-90到90度  
servo = AngularServo(6, min_angle=-90, max_angle=90)
while True:
    x = int(input('angle'))
    if x == 250 :
        break  
    
    servo.angle = x
    sleep(1)  

servo.close()