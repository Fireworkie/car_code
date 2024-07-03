import requests
from bs4 import BeautifulSoup
import re

# 发送网络请求获取页面内容
url = 'https://www.xueyinonline.com/detail/81070264'
response = requests.get(url)
html_content = response.text

# 使用Beautiful Soup解析页面内容
soup = BeautifulSoup(html_content, 'html.parser')

# 使用正则表达式提取enc的值
a = soup.find_all("script",attrs={"type":"text/javascript"})
for ai in a:
    enc_pattern = re.compile(r'endtime: "(.{19})')
    match = enc_pattern.search(str(ai.string))
    if match:
        matched_content = match.group(1)
        print("匹配到的30位内容:",matched_content)

            

