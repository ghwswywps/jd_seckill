# jd_seckill  

  
感谢 jsxzBillLee的贡献  
需要 python3   
需要 pip3 install requests beautifulsoup4 html5lib   
需要cookie中的thor   

请将rep_url修改成自己想要的3080搜索链接 目前已经无法保证一定可以框定自营原价商品  
推荐：  
TUF OC  
https://search.jd.com/search?keyword=3080%20tuf%20oc&qrst=1&suggest=2.def.0.base&wq=3080%20tuf%20oc&shop=1&ev=exbrand_%E5%8D%8E%E7%A1%95%EF%BC%88ASUS%EF%BC%89%5E296_136030%5Eexprice_0-6299%5E  
ADOC  
https://search.jd.com/search?keyword=3080&qrst=1&wq=3080&shop=1&ev=exbrand_%E4%B8%83%E5%BD%A9%E8%99%B9%EF%BC%88Colorful%EF%BC%89%5E296_136030%5Eexprice_6299-6299%5E  

本人抢到的是tuf oc，个人认为目前只有这两款比较值，不过如果tuf设置限定会员抢购此脚本可能会失效。

最近写了一套亚马逊PS5/XSX 到货监控，为了防止亚马逊识别风控，暂时闭源，需要提醒的兄弟关注微信公众号pushplus并且在pushplus.hxtrip.com获取token发至我的邮箱：  
i@abigant.com

-----
目前已知bug：
~~1.重复加入购物车(已定位)~~
~~2.低概率出现无法获取预购链接的问题~~
有时间修

-----

写在前面，感谢一位老哥提醒，如果担心自己号被黑，可以使用异地vps加新手机号抢购。如果还担心安全可以停止使用或者自行购入‘安全’的脚本，虽然我也不知道在哪买。  
声明此脚本只用于抢购3080 其他的需求请自行修改（很简单提示 'self.rep_url'），不提供教程  
未来不会更新功能，有bug尽量修复，如果未来jd修改api协议或有单独要求，会废弃此项目。  
目前抢3080的都是神仙，只能说神仙碰撞各凭本事，此脚本只抢购成功非热门商品，目前我开了3号抢了2次都在100毫秒内返回无货(可以说不做神仙基本无可能)，包括境内境外ip，前面肯定有一层随机算法，大家心态要放平。  

-----
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

~~修改成config配置模式~~  
~~增加多线程多账号支持~~  
增加了简单监控  
淦tm的黄牛  
~~更新了近几天的京东3080预约~~  

-----

修复bug 用类unix使用体验最佳


-----

不用配置秒杀配置了只需要设置thor即可自动预约+抢购近期所有的京东自营3080 （~~thor时间过长可能会失效~~）  
需要 pip3 install requests beautifulsoup4 html5lib

-----
此次更新后，可以保持thor长时间不失效了，增加1小时扫描一次是否有新3080上架并自动预约抢购，现在可以nohup后台运行了
如果遇到html解析器报错的问题(一般是py3环境问题) 可以全文删除 `features='html5lib'` 这个参数 不影响脚本。  

效果:  
![1](https://github.com/ghwswywps/jd_seckill/blob/master/run.png?raw=true)
![2](https://github.com/ghwswywps/jd_seckill/blob/master/to.png?raw=true)
