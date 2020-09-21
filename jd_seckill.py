#!/usr/bin/python2.6  
# -*- coding: utf-8 -*- 

import requests
import time
import json


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


        timeArray = time.strptime(self.order_time, "%Y-%m-%d %H:%M:%S")
        self.order_time_st = int(time.mktime(timeArray))


    def login(self): 
        JD.headers['referer'] = 'https://cart.jd.com/cart.action'
        c = requests.cookies.RequestsCookieJar()
        c.set('thor', self.thor)  
        self.session.cookies.update(c)
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip('jsonpUserinfo()\n')
        user_info = json.loads(response)
        print('账号：', user_info.get('nickName'))
        if user_info.get('nickName'):
            while True:
                time.sleep(self.gap)
                if time.time() <= self.order_time_st:
                    continue
                try:
                    if self.retry_limit < 1 :
                        pass
                    self.shopping()
                    self.retry_limit = self.retry_limit - 1
                except BaseException:
                    continue
                pass

    def shopping(self):
        self.goods_id = self.goods_url[
            self.goods_url.rindex('/') + 1:self.goods_url.rindex('.')]
        JD.headers['referer'] = self.goods_url
        buy_url = self.buy_url.format(self.goods_id)
        self.session.get(url=buy_url, headers=JD.headers)  

        self.session.get(url=self.pay_url, headers=JD.headers) 

        response = self.session.post(
            url=self.pay_success, headers=JD.headers)     
        print(response.text)
        order_id = json.loads(response.text).get('orderId')
        if order_id:
            print('抢购成功订单号:', order_id)

jd = JD()
jd.login()	

  
