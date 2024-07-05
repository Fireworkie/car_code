import os
import cv2
import requests
import json
import time
import socket
from aip import AipBodyAnalysis
from threading import Thread

APP_ID = '74238573'
API_KEY = 'F3Xlt3p4dqLThBf0JQEv8AIW'
SECRET_KEY = 'UfQRgEUHD3EqbG5uAP0pNnfBPE1bPnsC'
''' 调用'''

def send_command(command, server_ip='localhost', server_port=8001):
    """发送命令到服务器"""
    # 创建一个socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 连接到服务器
        client_socket.connect((server_ip, server_port))
        
        # 准备要发送的命令为JSON格式
        command_data = {"command": command}
        json_data = json.dumps(command_data)
        
        # 发送JSON数据到服务器
        client_socket.sendall(json_data.encode())
        
        print(f"命令 '{command}' 已发送至服务器")
        
        # 可以选择接收服务器的响应，如果有的话
        # response = client_socket.recv(1024).decode()
        # print("服务器响应:", response)
        
    except Exception as e:
        print(f"连接或发送命令时出现错误: {e}")
    finally:
        # 关闭客户端socket
        client_socket.close()

gestures = {'One': '数字1', 'Five': '数字5', 'Fist': '拳头', 'Ok': 'OK',
        'Prayer': '祈祷', 'Congratulation': '作揖', 'Honour': '作别',
        'Heart_single': '比心心', 'Thumb_up': '点赞', 'Thumb_down': 'Diss',
        'ILY': '我爱你', 'Palm_up': '掌心向上', 'Heart_1': '双手比心1',
        'Heart_2': '双手比心2', 'Heart_3': '双手比心3', 'Two': '数字2',
        'Three': '数字3', 'Four': '数字4', 'Six': '数字6', 'Seven': '数字7',
        'Eight': '数字8', 'Nine': '数字9', 'Rock': 'Rock', 'Insult': '竖中指', 'Face': '脸'}

gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=F3Xlt3p4dqLThBf0JQEv8AIW&client_secret=UfQRgEUHD3EqbG5uAP0pNnfBPE1bPnsC'
response = requests.get(host, verify=False)
if response.status_code != 200:
    print(f"Request failed with status {response.status_code}")
    print(response.text)  # 打印响应文本，看是否有错误信息
    exit()
print(response.text)
if response:
    print(response.json())
    token = response.json()['access_token']

def get_file_content(filePath): 
    """读取图片"""
    with open(filePath, 'rb') as fp: 
        return fp.read()

cap = cv2.VideoCapture(0)
cap.set(3,352)
cap.set(4,288)
# frame_num = 0

while cap.isOpened():
    ret,frame = cap.read()
    if  True:
        # frame_num=0
        cv2.imwrite('gesture.jpg',frame)
        image = get_file_content('gesture.jpg')

        message = gesture_client.gesture(image)
        print(message)
        num = message['result_num']
        if num == 0:
            print('没有识别到手势')
            # cv2.imshow("gesture",frame)
        else:
            results = message['result']
            content = []
            print(' ')
            for i, result in enumerate(results):
                classname = result['classname']
                print('识别结果为%s,'%(gestures[classname]))
                gesture = gestures[classname]
                if gesture == u'数字1':  #前进
                    send_command('forward')
                elif gesture == u'数字2':  #后退
                    send_command('backward')
                elif gesture == u'数字3':  #左转
                    send_command('left')
                elif gesture == u'数字4':  #右转
                    send_command('right')
                elif gesture == u'数字6':  #加速
                    send_command('speedup')
                    time.sleep(1)
                elif gesture == u'数字7':  #减速
                    send_command('speeddown')
                    time.sleep(1)
                elif gesture == u'数字5':  #停止
                    send_command('stop')
                #cv2.rectangle(frame, (result['left'],result['top']),(result['left'] + result['width'],result['top'] + result['height']),(255,255,255),2)
                #cv2.imshow("gesture",frame)
    time.sleep(0.3)
    # frame_num += 1

cap.release()
# cv2.destroyWindow("gesture")
