import os
import cv2
import requests
from aip import AipBodyAnalysis
from threading import Thread

APP_ID = '74238573'
API_KEY = 'F3Xlt3p4dqLThBf0JQEv8AIW'
SECRET_KEY = 'UfQRgEUHD3EqbG5uAP0pNnfBPE1bPnsC'
''' 调用'''

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
frame_num = 0

while cap.isOpened():
    ret,frame = cap.read()
    if frame_num % 5 == 0:
        cv2.imwrite('gesture.jpg',frame)
        image = get_file_content('gesture.jpg')

        message = gesture_client.gesture(image)
        print(message)
        num = message['result_num']
        if num == 0:
            print('没有识别到手势')
            cv2.imshow("gesture",frame)
        else:
            results = message['result']
            content = []
            print(' ')
            for i, result in enumerate(results):
                classname = result['classname']
                print('识别结果为%s,'%(gestures[classname]))
                cv2.rectangle(frame, (result['left'],result['top']),(result['left'] + result['width'],result['top'] + result['height']),(255,255,255),2)
                cv2.imshow("gesture",frame)

    frame_num += 1

    if cv2.waitKey(200) & 0xff == 27:
        break

cap.release()
cv2.destroyWindow("gesture")