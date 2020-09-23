# jd_seckill

因一位老哥提醒，如果担心自己号被黑，可以使用异地vps加新手机号抢购  

被京东3080耍猴搞吐了，只能自己搞个，需要的拿走
需要python3

需要配置的如下
        ~~1.cookie 2.url 3.秒杀时间 4.秒杀总次数限制 5.秒杀请求间隙~~
        
 ~~self.thor = ''~~	
 ~~self.goods_url = 'https://item.jd.com/10021776150443.html'~~
 ~~self.order_time = '2020-09-21 20:30:00'~~
 ~~self.retry_limit = 20~~
 ~~self.gap = 0.1~~
        
目前只需要thor配置

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

-----
此次更新后，可以保持thor长时间不失效了，增加1小时扫描一次是否有新3080上架并自动预约抢购，现在可以nohup后台运行了
如果遇到html解析器报错的问题(一般是py3环境问题) 可以全文删除 `features='html5lib'` 这个参数 不影响脚本。  

效果:  
![1](https://github.com/ghwswywps/jd_seckill/blob/master/run.png?raw=true)
![2](https://github.com/ghwswywps/jd_seckill/blob/master/to.png?raw=true)
