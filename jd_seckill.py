#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import requests
import time
import json
import os
import copy
import _thread

config = {
    '七彩虹 AD 3080':{
        'thor':'',
        'goods_url':'https://item.jd.com/100015062680.html',
        'order_time':'2020-09-21 20:30:00',
    }
}

LOG_TEMPLE_BLUE='\033[1;34m{}\033[0m '
LOG_TEMPLE_RED='\033[1;31m{}\033[0m '
LOG_TEMPLE_SUCCESS='\033[1;32mSUCCESS\033[0m '
LOG_TEMPLE_FAILED='\033[1;31mFAILED\033[0m '

class JD:
    headers = {
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    def __init__(self):
        self.index = 'https://www.jd.com/'
        self.user_url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?&callback=jsonpUserinfo&_=' + \
            str(int(time.time() * 1000)) 
        self.buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'   
        self.pay_url = 'https://cart.jd.com/gotoOrder.action'  
        self.pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'  
        self.goods_id = ''  
        self.session = requests.session()

        # 配置项 只要填这5个 1.cookie 2.url 3.秒杀时间 4.秒杀总次数限制 5.秒杀请求间隙
        self.thor = ''	
        self.goods_url = 'https://item.jd.com/10021776150443.html'
        self.order_time = '2020-09-21 20:30:00'
        self.retry_limit = 20
        self.gap = 0.1
        


    def login(self): 
        JD.headers['referer'] = 'https://cart.jd.com/cart.action'
        c = requests.cookies.RequestsCookieJar()
        c.set('thor', self.thor)  
        self.session.cookies.update(c)
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip('jsonpUserinfo()\n')
        self.user_info = json.loads(response)
        if self.user_info.get('nickName'):
            for key in config:
                item = copy.copy(self)
                timeArray = time.strptime(config[key]['order_time'], "%Y-%m-%d %H:%M:%S")
                order_time_st = int(time.mktime(timeArray))
                item.order_time_st = order_time_st
                config[key]['order_time_st'] = order_time_st
                item.thor = config[key]['thor']
                item.goods_url = config[key]['goods_url']
                item.order_time = config[key]['order_time']
                _thread.start_new_thread( self.run, (item, ))
                pass
            _thread.start_new_thread(self.log,())
            pass
            
    def log(self):
        clock = round(time.time())
        while True:
            time.sleep(0.1)
            r = round(time.time())
            if r > clock:
                clock = r
                print('\x1b[H\x1b[2J')
                log = []
                log.append(LOG_TEMPLE_BLUE.format('账号') + self.user_info.get('nickName') + '\n\n')

                for key in config:
                    if time.time() <= config[key]['order_time_st']:
                        log.append('\t\t' + LOG_TEMPLE_RED.format(key) + '\n')
                        log.append(LOG_TEMPLE_BLUE.format('抢购时间')  + config[key]['order_time'] + '\n')
                        log.append(LOG_TEMPLE_BLUE.format('剩余时间')  + str(round(config[key]['order_time_st'] - r, 2)) + '秒\n\n')

                print(''.join(log))
            
            pass
        pass

    def run(self, item):
        while True:
            time.sleep(item.gap)
            if time.time() <= item.order_time_st:
                continue
            try:
                if item.retry_limit < 1 :
                    return
                
                o = item.shopping(item)
                if o:
                    return
                item.retry_limit = item.retry_limit - 1
            except BaseException:
                continue
        pass

    def shopping(self, item):
        item.goods_id = item.goods_url[
            item.goods_url.rindex('/') + 1:item.goods_url.rindex('.')]
        JD.headers['referer'] = item.goods_url
        buy_url = item.buy_url.format(item.goods_id)
        item.session.get(url=buy_url, headers=JD.headers)  

        item.session.get(url=item.pay_url, headers=JD.headers) 

        response = item.session.post(
            url=item.pay_success, headers=JD.headers)
        order_id = json.loads(response.text).get('orderId')
        if order_id:
            print('抢购成功订单号:', order_id)
            return True

jd = JD()
jd.login()	

while 1:
    pass

  
