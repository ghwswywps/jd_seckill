# jd_seckill

被京东3080耍猴搞吐了，只能自己搞个，需要的拿走
需要python3

需要配置的如下
        1.cookie 2.url 3.秒杀时间 4.秒杀总次数限制 5.秒杀请求间隙
        
        self.thor = ''	
        self.goods_url = 'https://item.jd.com/10021776150443.html'
        self.order_time = '2020-09-21 20:30:00'
        self.retry_limit = 20
        self.gap = 0.1
        
        
-----

修改成config配置模式  
增加多线程多账号支持  
增加了简单监控  
淦tm的黄牛  
更新了近几天的京东3080预约  

-----

修复bug 用类unix使用体验最佳


-----

不用配置秒杀配置了只需要设置thor即可自动预约+抢购近期所有的京东自营3080 （thor时间过长可能会失效）  
需要 pip3 install requests beautifulsoup4 html5lib
