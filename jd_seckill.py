#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import requests
import time
import json
import os
import copy
import _thread
from bs4 import BeautifulSoup
#cookie，可以在我的订单页面，搜索list的网络请求，获取cookie值
thor = ''
#日志模板，有颜色和状态
LOG_TEMPLE_BLUE='\033[1;34m{}\033[0m '
LOG_TEMPLE_RED='\033[1;31m{}\033[0m '
LOG_TEMPLE_SUCCESS='\033[1;32mSUCCESS\033[0m '
LOG_TEMPLE_FAILED='\033[1;31mFAILED\033[0m '

class JD:
    headers = {
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    #初始化配置
    def __init__(self):
        self.index = 'https://www.jd.com/'

        self.clock_url = 'https://a.jd.com//ajax/queryServerData.html'
        #用户信息获取地址
        self.user_url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action?&callback=jsonpUserinfo&_=' + \
            str(int(time.time() * 1000)) 
        #加购物车
        self.buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'   
        #修改购物车商品数量为1
        self.change_num = 'https://cart.jd.com/changeNum.action?pid={}&pcount=1&ptype=1'
        #下单
        self.pay_url = 'https://cart.jd.com/gotoOrder.action'  
        #订单提交
        self.pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'  
        #商品id
        self.goods_id = ''  
        #会话
        self.session = requests.session()

        #3080搜索链接
        self.rep_url = 'https://search.jd.com/search?keyword=3080&qrst=1&wq=3080&shop=1&ev=exbrand_%E4%B8%83%E5%BD%A9%E8%99%B9%EF%BC%88Colorful%EF%BC%89%5E296_136030%5Eexprice_6299-6299%5E'
        #耕升3080追风
        self.g_url = 'https://item.jd.com/100015062658.html'
        #商品详情地址
        self.item_info_url = 'https://item-soa.jd.com/getWareBusiness?skuId={}'
        #预约地址
        self.appoint_url = ''
        self.config = {}

        #cookie
        self.thor = thor
        #重试次数限制
        self.retry_limit = 100
        #重试间隔
        self.gap = 0.1
        #重试计数
        self.retry_count = 0
        #本地时间与京东时间差
        self.time_diff = 0.1
        
    def initTime(self):
        ret = requests.get(self.clock_url).text
        js = json.loads(ret)
        self.time_diff = js.get('serverTime')/1000 - time.time() + 0.001

    #登录，然后抢预约成功的商品
    def buy(self): 
        #1通过session获取用户信息
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip('jsonpUserinfo()\n')
        #1.1调用内置的loads方法获取json格式的用信息
        self.user_info = json.loads(response)
        if self.user_info.get('nickName'):
            #遍历预约成功的商品，挨个抢购
            for key in self.config:
                item = copy.copy(self)
                #下单时间（使用本机时间，记得和京东服务器同步时间）
                timeArray = time.strptime(self.config[key]['order_time'], "%Y-%m-%d %H:%M")
                order_time_st = int(time.mktime(timeArray))
                item.order_time_st = order_time_st
                self.config[key]['order_time_st'] = order_time_st
                item.goods_url = self.config[key]['goods_url']
                item.order_time = self.config[key]['order_time']
                _thread.start_new_thread( self.run, (item, ))
                pass
            _thread.start_new_thread(self.log,())
            pass

            
    #日志方法
    def log(self):
        clock = round(time.time())
        i = 0
        while True:
            time.sleep(0.1)
            r = round(time.time())
            if r > clock:
                i += 1
                clock = r
                print('\x1b[H\x1b[2J')
                log = []
                log.append(LOG_TEMPLE_BLUE.format('账号') + self.user_info.get('nickName') + '\n\n')

                for key in self.config:
                    if time.time() <= self.config[key]['order_time_st']:
                        log.append('\t\t' + LOG_TEMPLE_RED.format(key) + '\n')
                        log.append(LOG_TEMPLE_BLUE.format('抢购时间')  + self.config[key]['order_time'] + '\n')
                        log.append(LOG_TEMPLE_BLUE.format('剩余时间')  + str(round(self.config[key]['order_time_st'] - r, 2)) + '秒\n\n')

                print(''.join(log))
                if i > 3600:
                    print('开始扫描是否有新增3080商品...')
                    self.rep()
                    self.appoint()
                    i = 0           
            pass
        

    def run(self, item):
        while True:
            time.sleep(item.gap)
            if time.time() + self.time_diff <= item.order_time_st:
                continue
            try:
                if item.retry_limit < 1 :
                    return
                
                o = item.shopping(item)
                
                if o:
                    return
                item.retry_limit = item.retry_limit - 1
                #重试计数
                item.retry_count = item.retry_count + 1
            except BaseException:
                continue
        

    def shopping(self, item):
        #获取商品id，从url的/开始位置截取到.位置
        item.goods_id = item.goods_url[
            item.goods_url.rindex('/') + 1:item.goods_url.rindex('.')]
        JD.headers['referer'] = item.goods_url
        # url格式化，把商品id填入buy_url
        buy_url = item.buy_url.format(item.goods_id)
        #get请求，添加购物车
        item.session.get(url=buy_url, headers=JD.headers)  
        #修正购物车商品数量（第二次重试后修正购物车数量）
        if item.retry_count > 0 :
            print('第',item.retry_count,'次重试，抢购商品为：',item.goods_id,'修正购物车商品数量。')
            change_num_url = item.change_num.format(item.goods_id)
            item.session.get(url=change_num_url, headers=JD.headers)
        #get请求
        item.session.get(url=item.pay_url, headers=JD.headers) 
        #post请求，提交订单
        response = item.session.post(
            url=item.pay_success, headers=JD.headers)
        order_id = json.loads(response.text).get('orderId')
        if order_id:
            print('抢购成功订单号:', order_id)
            return True

    def rep(self):
        JD.headers['referer'] = 'https://cart.jd.com/cart.action'
        c = requests.cookies.RequestsCookieJar()
        c.set('thor', self.thor)  
        self.session.cookies.update(c)
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip('jsonpUserinfo()\n')
        self.user_info = json.loads(response)
        if not self.user_info.get('nickName'):
            raise Exception("账号验证错误请检查thor")

        p = self.session.get(url=self.rep_url, headers=JD.headers) 
        bf = BeautifulSoup(p.text, features='html5lib')
        texts = bf.find_all('div', class_ = 'p-name p-name-type-2') 
        for text in texts:
            time.sleep(0.2)
            rtx = {}
            rtx['title'] = text.em.text.replace('\n','')
            if rtx['title'] in self.config:
                continue
            rtx['goods_url'] = 'https:' + text.a['href']
            jid = rtx['goods_url'] [rtx['goods_url'].rindex('/') + 1:rtx['goods_url'].rindex('.')]
            p = self.session.get(url=self.item_info_url.format(jid), headers=JD.headers)
            if p.text:
                try:
                    yyinfo = json.loads(p.text).get('yuyueInfo')
                    if yyinfo:
                        rtx['appoint_url'] = yyinfo['url']
                        rtx['order_time'] = yyinfo['buyTime'].split('-202')[0]
                        self.config[rtx['title']] = rtx
                        rtx['appoint'] = False
                        print('正在添加如下商品：' + rtx['title'])
                        pass
                    pass
                except BaseException:
                    print(p.text)


    
    def appoint(self):
        print('开始预约\n')
        for key in self.config:
            if not self.config[key]['appoint']:
                if not self.config[key]['appoint_url']:
                    continue
                ares = self.session.get(url='https:' + self.config[key]['appoint_url'], headers=JD.headers)
                bf = BeautifulSoup(ares.text, features='html5lib')
                texts = bf.find_all(class_ = 'bd-right-result')
                if len(texts) > 0:
                    print(key + ' 预约结果：\n' + texts[0].text.strip())
                    self.config[key]['appoint'] = True
                else:
                    print(LOG_TEMPLE_RED.format(key + '\n需要手动预约：') + LOG_TEMPLE_BLUE.format('https:' + self.config[key]['appoint_url']))
                print('--------------------------')  
        for i in range(10):
            time.sleep(1) 
            end_str = '100%'
            print('\r' + str(10 - i) + '秒后进入监控页面，若需要手动预约请CTRL+C退出脚本预约后再执行...', end='', flush=True)


jd = JD()
jd.rep()
jd.appoint()
jd.buy()	


while 1:
    time.sleep(10)

