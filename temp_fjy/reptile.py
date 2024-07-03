import requests 
from bs4 import BeautifulSoup
import psycopg2
from urllib.parse import urljoin
import json
import re
conn = psycopg2.connect(database='fanya_class',user='postgres',password='147528',host='localhost',port='5432')
cur = conn.cursor()
#cur.execute('TRUNCATE TABLE fanya_classdata')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
content = "https://fanya.chaoxing.com/fanya/courselist?fcId=5&scId=6&modalityId=0&sort=1"
content1 =requests.get(content,headers=headers).text
soup =BeautifulSoup(content1,"html.parser")
all_count1 = soup.find_all("dd",attrs={"class":"fs14"})  #爬课程名字和课程人数的
all_count2 = soup.find_all("dd",attrs={"class":"fs12"}) #爬学校和老师的
all_count3 = soup.find_all("a",attrs={"class":"licura"})
all_address = soup.find_all("div",attrs={"class":"Wm3CT1"})
for i1, i2, tag in zip(all_count1, all_count2, all_address):
    subject = i1.string#获得学科
    attending_count = i2.find("i").string#获得参与人数
    teacher_and_school = i2.find("span").string
    cleaned_text = ' '.join(teacher_and_school.split())  # 去除多余的空格和换行符
    cleaned_text_str = cleaned_text.replace(' ', '\\')
    teacher_and_school = cleaned_text_str
    degree = all_count3[0].text#获得学历
    major = all_count3[1].text#获得专业
    a_tags = tag.find_all('a')
    subject_info = (subject, attending_count, degree, major)
    for a_tag in a_tags:
        booknames=[]
        courseoutlines=[]
        href_content = a_tag.get('href')
        full_url = urljoin(content, href_content)#获得课程全地址
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        html_content3 = requests.get(full_url, headers=headers).text
        soup = BeautifulSoup(html_content3, "html.parser")
        all_count6 = soup.find_all("iframe", attrs={"class": "ans-insertbook-module"})
        for iframe in all_count6:
                data_attr = iframe.get('data')
                data_json = json.loads(data_attr)
                bookname = data_json.get('bookname')#获得课程需要的教材（全部）
                booknames.append(bookname)
        all_count7 = soup.find_all("div", attrs={"class": "chapterText"})
        all_count7i = soup.find_all("td",attrs={"class":"pt10 g6 resources_td"})
        if not all_count7 and not all_count7i:
            div_tag = soup.find('input', id='courseId')
            if div_tag:
                outline_lists1=[]
                outline_lists1i=[]
                data_value = div_tag.get('value')
                origin1 = "https://www.xueyinonline.com/detail/knowledge-catalog"
                params1 = {'courseId': '81120769','orgCourseId': '81120769'}        
                params1['courseId'] = str(data_value)
                params1['orgCourseId'] = str(data_value)
                origin2 = 'https://www.xueyinonline.com/course/getevaluate?courseid=81070264&enc=67cd3e1becc05ef577cb6845fb9dc777&starttime="2019-02-18 00:00:00"&endtime= "2019-07-04 23:59:59",&size= 50'
                params2 ={'courseid': '81070264',
                'enc': "67cd3e1becc05ef577cb6845fb9dc777",
                'starttime': "2019-02-18 00:00:00",
                'endtime': "2019-07-04 23:59:59",
                'size': 50}
                all_count7ii = soup.find_all("script",attrs={"type":"text/javascript"})
                for ai in all_count7ii:
                    enc_pattern = re.compile(r'enc: "(.{32})')
                    starttime_pattern = re.compile(r'starttime: "(.{19})')
                    endtime_pattern = re.compile(r'endtime: "(.{19})')
                    match1 = enc_pattern.search(str(ai.string))
                    match2 = starttime_pattern.search(str(ai.string))
                    match3 = endtime_pattern.search(str(ai.string))
                    if match1 and match2 and match3:
                        enc = match1.group(1)
                        starttime = match2.group(1)
                        endtime = match3.group(1)
                        params2['courseid'] = str(data_value)
                        params2["enc"] = enc
                        params2["starttime"] = starttime
                        params2["endtime"] = endtime 
                html_content1 = requests.get(origin1, params=params1).text
                html_content2 = requests.get(origin2,params =params2).text
                soup = BeautifulSoup(html_content1, 'html.parser')
                course_catalog_element = soup.find(class_="mkCata")
                course_catalog = course_catalog_element.get_text()
                outline_lists1.append(course_catalog)
                cleaned_text1 = [' '.join(outline_list.split()) for outline_list in outline_lists1]  # 去除多余的空格和换行符
                cleaned_text_str1 = '\\n'.join(cleaned_text1) 
                soup = BeautifulSoup(html_content2,'html.parser')
                course_big_num =soup.find(class_="big_num")
                if not course_big_num:
                    cur.execute('INSERT INTO fanya_classdata(subject, attending_count, degree, major, class_address,teacher_and_school,comment_count,book,course_outline) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)', (subject, attending_count, degree, major, full_url,teacher_and_school,None,booknames,cleaned_text_str1))
                else:
                    course_num = course_big_num.get_text()
                    outline_lists1i.append(course_num)
                    cur.execute('INSERT INTO fanya_classdata(subject, attending_count, degree, major, class_address,teacher_and_school,comment_count,book,course_outline) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)', (subject, attending_count, degree, major, full_url,teacher_and_school,None,booknames,outline_lists1))
        elif not all_count7i:
            outline_lists2=[]
            for i7 in all_count7:
                outline_lists2.append(i7.string)
                outline_str2 = ' '.join(outline_lists2)
                div_tag = soup.find('div', id='courseStarTag')
                if div_tag:
                    data_value = div_tag.get('data')
                    origin = "https://mooc1.chaoxing.com/mooc-ans/coursestar?courseId=80446176&edit=false"
                    new_url = origin.replace("80446176", str(data_value))
                    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    response = requests.get(new_url, headers=headers).text
                    soup = BeautifulSoup(response, "html.parser")
                    all_count4 = soup.find_all("i", attrs={"class": "zev_sc_fs"})
                    all_count5 = soup.find_all("span", attrs={"id": "avg_d"})
                    for i4,i5 in zip(all_count4,all_count5):
                        comment_count =i4.string+i5.string
                        cur.execute('INSERT INTO fanya_classdata(subject, attending_count, degree, major, class_address,teacher_and_school,comment_count,book,course_outline) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)', (subject, attending_count, degree, major, full_url,teacher_and_school,comment_count,booknames,outline_str2))
        else:
            outline_lists3 =[]
            for i7i in all_count7i:
                outline_lists3.append(i7i.string)
                outline_str3 = ' '.join(outline_lists3)
            div_tag = soup.find('div', id='courseStarTag')
            if div_tag:
                data_value = div_tag.get('data')
                origin = "https://mooc1.chaoxing.com/mooc-ans/coursestar?courseId=80446176&edit=false"
                new_url = origin.replace("80446176", str(data_value))
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(new_url, headers=headers).text
                soup = BeautifulSoup(response, "html.parser")
                all_count4 = soup.find_all("i", attrs={"class": "zev_sc_fs"})
                all_count5 = soup.find_all("span", attrs={"id": "avg_d"})
                for i4,i5 in zip(all_count4,all_count5):
                    comment_count =i4.string+i5.string
                    cur.execute('INSERT INTO fanya_classdata(subject, attending_count, degree, major, class_address,teacher_and_school,comment_count,book,course_outline) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)', (subject, attending_count, degree, major, full_url,teacher_and_school,comment_count,booknames,outline_str3))
conn.commit()
cur.close()
conn.close()
