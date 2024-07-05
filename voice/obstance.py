import RPi.GPIO as GPIO
import socket
import time
import json



data={
    'command':'stop'
}
json_data=json.dumps(data).encode('utf-8')

def get_distance():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    trig = 16
    echo = 18

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    """返回到障碍物的距离"""
    # 向trig端发送10us高电平信号
    GPIO.output(trig, 1)
    start_time = time.time()
    time.sleep(0.00001)
    # 结束发送
    GPIO.output(trig, 0)
    # 通过echo端开始检测回声信号
    end_time = start_time
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
#    return distance
    return("前方障碍物距离{:.1f}厘米".format(distance))

if __name__ == "__main__":
    while True:
        distance = get_distance()
        print("Distance: {:.2f}cm".format(distance))
        if distance < 20 and distance!=0:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 8001))
            client_socket.sendall(json_data)
            client_socket.close()
        time.sleep(0.5)    
