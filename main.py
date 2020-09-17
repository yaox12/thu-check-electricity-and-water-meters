# -*- coding: utf-8 -*-
import re
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
from http.cookiejar import CookieJar

import config

# pylint: disable=C0103

def look_up_ele_and_water():
    BASE_URL = 'http://m.myhome.tsinghua.edu.cn/'
    LOGIN_URL = BASE_URL + 'Loginwindow.aspx'
    ELE_LOOKUP_URL = BASE_URL + 'weixin/weixin_student_electricity_search.aspx'
    WATER_LOOPUP_URL = BASE_URL + 'weixin/weixin_student_water_search.aspx'

    data = {'__VIEWSTATE': '/wEPDwUJMzUxODM3OTcwZGSzjX6gFtY6tdAxR1DJThQLsW0mqCd9bss+APDYXmKA8g==',
            '__VIEWSTATEGENERATOR': '4B45C1AF',
            'LoginCtrl1$txtUserName': config.username,
            'LoginCtrl1$txtPassword': config.password,
            'LoginCtrl1$btnLogin': '登录'}
    cookie = CookieJar()
    handler = HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    data = urlencode(data).encode('GBK')
    opener.open(Request(LOGIN_URL, data)).read().decode('GBK')

    def read_number(lookup_url):
        res = opener.open(Request(lookup_url, data)).read().decode('GBK')
        # with open('res.html', 'w') as f:
        #     f.write(res)

        num = -1
        for line in res.split('\n'):
            if 'lblele' in line:
                line = line.strip()
                get_num = re.compile(r'>(\d+)')
                num = int(get_num.findall(line)[0])

        return num

    ele = read_number(ELE_LOOKUP_URL)
    water = read_number(WATER_LOOPUP_URL)
    return ele, water

def send_email(ele, water):
    message = MIMEText(f'宿舍剩余电量：{ele}度，剩余热水：{water}元，请及时充值！', 'plain', 'utf-8')
    message['From'] = formataddr(('电量/热水查询bot', config.mail_username))
    message['To'] = ','.join(config.receivers)

    subject = '宿舍低电量/热水提醒'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(config.mail_host, 465)
        smtpObj.login(config.mail_username, config.mail_password)
        smtpObj.sendmail(config.mail_username, config.receivers, message.as_string())
        smtpObj.quit()
        print('Email succeed')
    except smtplib.SMTPException:
        print('Email failed')

def main():
    print(datetime.datetime.now())
    ele, water = look_up_ele_and_water()
    print(f'剩余电量：{ele}度，剩余热水：{water}元。')
    if ele < 50 or water < 15:
        send_email(ele, water)
    print()

if __name__ == '__main__':
    main()
