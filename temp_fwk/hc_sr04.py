import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
# 指定Trig和Echo的引脚编号
trig = 16
echo = 18
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
i = 0
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
if __name__ == '__main__':
    try:
        while True:
            distance = get_distance()
            print("距离是：", distance)
            time.sleep(2)
    except KeyboardInterrupt:
        print("程序结束！")
    finally:
        GPIO.cleanup()