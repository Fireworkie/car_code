import os
import time
import json
import socket
import requests
from aip import AipBodyAnalysis
from aip import AipSpeech
from dht11 import read_dht11
import RPi.GPIO as GPIO
#from north import to_north
from obstance import get_distance

# 百度语音识别API配置
APP_ID = '74238573'
API_KEY = 'ooFzrw8c7HCxCKWBez26SFcc'
SECRET_KEY = 'FMYy279RdHWjYal5fWNMmRR7uWAhzLMc'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ooFzrw8c7HCxCKWBez26SFcc&client_secret=FMYy279RdHWjYal5fWNMmRR7uWAhzLMc'
response = requests.get(host, verify=False)
if response:
    print(response.json())
    token = response.json()['access_token']
    print(token)

def toPCM():
    os.system('arecord -d 3 -r 16000 -c 1 -t wav -f S16_LE voice.wav')
    os.system('ffmpeg -y -i voice.wav -acodec pcm_s16le -f s16le -ac 1 -ar 16000 voice.pcm')

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def getVoice():
    if os.path.exists('voice.pcm'):
        results = client.asr(get_file_content('voice.pcm'), 'pcm', 16000, {'dev_pid': 1537,})
        voice = results['result'][0]
        return voice

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

if __name__ == '__main__':
    while True:
        GPIO.cleanup()
        print("开始录音（“前进，后退，左转，右转，加速，减速，停止”）...")
        toPCM()
        print("录音结束，开始识别...")
        # time.sleep(3)
        voice = getVoice()
        print("识别结果：", voice)
#    if voice == u'前进。':
#        send_command('forward')
#    elif voice == u'后退。':
#        send_command('backward')
#    elif voice == u'左转。':
#        send_command('left')
#    elif voice == u'右转。':
#        send_command('right')
#    elif voice == u'加速。':
#        send_command('speedup')
#        time.sleep(1)
#    elif voice == u'减速。':
#        send_command('speeddown')
#        time.sleep(1)
#    elif voice == u'停止。':
#        send_command('stop')
        if voice == u'检测温湿度。':
            data = read_dht11()
            print(data)
            url = '\"' + 'https://tsn.baidu.com/text2audio?tex=' + '\"' + data + '\"' + "&lan=zh&per=0&pit=7&spd=5&cuid=1234567890123456&ctp=1&tok=" + token + '\"'
            os.system("ffplay -vn -autoexit " + "%s"%(url))
#        elif voice == u'小车朝北。':
#            to_north()
#            url = '\"' + 'https://tsn.baidu.com/text2audio?tex=' + '\"' + '小车已朝北' + '\"' + "&lan=zh&per=0&pit=7&spd=5&cuid=1234567890123456&ctp=1&tok=" + token + '\"'
#            os.system("ffplay -vn -autoexit " + "%s"%(url))
        elif voice == u'测距。':
            data = get_distance()
            print(data)
            url = '\"' + 'https://tsn.baidu.com/text2audio?tex=' + '\"' + '当前距离为' + data + '\"' + "&lan=zh&per=0&pit=7&spd=5&cuid=1234567890123456&ctp=1&tok=" + token + '\"'
            os.system("ffplay -vn -autoexit " + "%s"%(url))
        elif voice == u'退出。':
            url = '\"' + 'https://tsn.baidu.com/text2audio?tex=' + '\"' + '已退出'  + '\"' + "&lan=zh&per=0&pit=7&spd=5&cuid=1234567890123456&ctp=1&tok=" + token + '\"'
            os.system("ffplay -vn -autoexit " + "%s"%(url))
            break
        else:
            print("未识别到命令")
