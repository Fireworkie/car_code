import os
import requests
from aip import AipBodyAnalysis
import sys

APP_ID = '74238573'
API_KEY = 'ooFzrw8c7HCxCKWBez26SFcc'
SECRET_KEY = 'FMYy279RdHWjYal5fWNMmRR7uWAhzLMc'

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ooFzrw8c7HCxCKWBez26SFcc&client_secret=FMYy279RdHWjYal5fWNMmRR7uWAhzLMc'
response = requests.get(host, verify=False)
if response:
    print(response.json())
    token = response.json()['access_token']
    print(token)

    url = '\"' + 'https://tsn.baidu.com/text2audio?tex=' + '\"' + sys.argv[1] + '\"' + "&lan=zh&per=0&pit=7&spd=5&cuid=1234567890123456&ctp=1&tok=" + token + '\"'
    os.system("ffplay -vn -autoexit " + "%s"%(url))