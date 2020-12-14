'''
    京东时间同步for windows
    需要安装win32api和requests
    pip install pypiwin32
    pip install requests
'''
import time
from datetime import datetime
import requests
import json
import os

from sys import platform

if platform == 'win32' or platform == 'win64':
    import win32api

def getTime():
    url = 'https://a.jd.com//ajax/queryServerData.html'
    ret = requests.get(url).text
    js = json.loads(ret)
    #print(float(js.get('serverTime'))/1000)
    return float(js.get('serverTime')/1000)

def setSystemTimeWin():
    jd_time = getTime()
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(jd_time)
    #strTime = datetime.strftime(datetime.fromtimestamp(getTime()),'%Y-%m-%d %H:%M:%S.%f')
    #msec = strTime
    strTime = datetime.strftime(datetime.fromtimestamp(jd_time),'%Y-%m-%d %H:%M:%S.%f')
    msec = int(float(datetime.strftime(datetime.fromtimestamp(jd_time),'%f'))/1000);
    print(strTime)
    print('msec：',msec)

def setSystemTimeUnix():
        cmd = "date -s @" + str(getTime())
        #print(cmd)
        os.system(cmd)

def setSystemTime():
    if platform == 'win32' or platform == 'win64':
        setSystemTimeWin()
    elif platform == 'linux' or platform == 'linux2' or platform == 'darwin':
        setSystemTimeUnix()
    else:
        print("不支持时间同步：%s", platform)



if __name__ == '__main__':
    setSystemTime()  #运行一次后，在本条语句前加#注释后可以查看时间同步情况
    print("京东时间:%s\n本地时间:%s"%(datetime.fromtimestamp(getTime()),datetime.now()))
