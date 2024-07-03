import os
import time
import json
from aip import AipSpeech

# 百度语音识别API配置
APP_ID = '74238573'
API_KEY = 'ooFzrw8c7HCxCKWBez26SFcc'
SECRET_KEY = 'FMYy279RdHWjYal5fWNMmRR7uWAhzLMc'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def toDCM():
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


print("开始录音...")
toDCM()
print("录音结束，开始识别...")
time.sleep(3)
voice = getVoice()
print("识别结果：", voice)