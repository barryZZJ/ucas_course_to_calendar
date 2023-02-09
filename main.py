import os
import requests as r
from datetime import datetime
from bs4 import BeautifulSoup
import argparse

from coursecalendar import Calendar
from httpRequestUtil_contextmanager import httpRequest

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='courses')
args = parser.parse_args()

def error(msg):
    print(msg)
    os.system('pause')
    exit()

firstdayofterm = input("学期第一天的年月日，用'.'隔开，如2022.8.22：")
jsessionid = input('JSESSIONID：')

host = 'https://jwxk.ucas.ac.cn'
url = host + '/courseManage/main'

s = r.Session()
cookies = {
    'JSESSIONID': jsessionid # jwxk.ucas.ac.cn
}

firstday = datetime(*map(int, firstdayofterm.split('.')))
calendar = Calendar(firstday)

with httpRequest(s, url, 'get', cookies=cookies) as resp:
    # 解析"已选择课程"表格
    soup = BeautifulSoup(resp.content, 'html.parser')
    print('正在解析已选课程表格')
    table = soup.find('table')
    if not table:
        error('错误！无法解析已选课程表格，请检查jsessionid是否过期')
    for i, tr in enumerate(table.tbody.find_all('tr')):
        tds = tr.find_all('td')
        courseId = tds[0].a.getText()
        a_courseName = tds[1].a
        courseName = a_courseName.getText()
        courseTimeUrl = host + a_courseName['href']
        teacherName = tds[6].a.getText()
        print(f"{i+1:2}" + '. ' + courseId + '\t' + courseName)
        with httpRequest(s, courseTimeUrl, 'get') as resp2:
            # 解析上课时间
            soup2 = BeautifulSoup(resp2.content, 'html.parser')
            table2 = soup2.table
            if not table2:
                print('错误！无法获取课程时间表，暂时跳过。请确认选课系统中是否正确显示。')
                continue
            trs2 = table2.find_all('tr')
            groups = [(trs2[i].td.getText(), trs2[i+1].td.getText(), trs2[i+2].td.getText()) for i in range(0, len(trs2), 3)]
            for time, place, week in groups:
                calendar.appendCourse(courseId, courseName, time, place, week, teacherName)

print('解析完成，正在生成文件' + args.output + '.ics')
calendar.to_ics(args.output + '.ics')
print('成功！\n\n通过邮件等方式发送到手机后，即可导入到手机日历，安卓苹果通用。\n导入时建议新建一个日历账户，这样方便统一删除以及颜色区分。\n')
os.system('pause')


