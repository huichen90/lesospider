# -*- coding: utf-8 -*-
import json
import time
import scrapy

from lesospider.items import LesospiderItem



class LesoSpider(scrapy.Spider):
    name = 'leso'
    start_urls = ['http://www.leso.cn/']
    def __init__(self,keywords = '你好',limit=800,taskId = 4,*args,**kwargs):
        super(LesoSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        # keywords = 'hello'
        self.limit_time = limit
        self.task_id = taskId
        self.site_name = '乐视网'
        self.info ='无简介'
        self.video_category = '未分类'
        self.allowed_domains = ['www.leso.cn','search.lekan.letv.com','www.le.com']
        self.url1 = 'http://search.lekan.letv.com/lekan/apisearch_json.so?from=pc&jf=1&hl=1&dt=1,2&ph=420001,420002&' \
                    'show=4&ps=35&wd='+self.keywords+'&lc=d6e77564c06b615ab16616b24d3e2fbf&_=1526536864900&pn='

        self.page = 1
        self.start_urls = [self.url1+'1']

        # print('正在爬去第1页' )
    def parse(self, response):
        # print(response.text)
        video_list = json.loads(response.text)['data_list']
        # print(len(video_list))
        # print(video_list[0])
        item = LesospiderItem()
        item['limit_time'] = self.limit_time
        for video in video_list:


            item['tags'] = []
            item['site_name'] = video.get('source','乐视网')
            if item['site_name'] !='letv':
                item['url'] = video.get('url')
            else:
                item['url'] = 'http://www.le.com/ptv/vplay/' + video['vid'] + '.html'
            print(item['url'])
            item['keywords'] = self.keywords
            item['task_id'] = self.task_id
            item['video_category']= video.get('categoryName','')
            item['title'] = video.get('name','')
            item['play_count'] = video.get('playCount','')
            item['info'] = video.get('description','')
            item['video_time'] = video.get('duration','')
            time1 = video.get('releaseDate', '')
            if time1 !='':
                timestamp = int(time1[:10])
                time_local = time.localtime(timestamp)
                item['upload_time'] = time.strftime("%Y-%m-%d ", time_local)
            else:
                item['upload_time']=''

            yield item

        self.page += 1
        if self.page <= 8:
            print("开始爬去第%d页" % self.page)
            url = self.url1 + str(self.page)
            time.sleep(5)
            # 再次发送请求
            yield scrapy.Request(url=url, callback=self.parse)

