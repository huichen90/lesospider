# -*- coding: utf-8 -*-
import json

import scrapy

from lesospider.items import LesospiderItem



class LesoSpider(scrapy.Spider):
    name = 'leso'
    start_urls = ['http://www.leso.cn/']
    def __init__(self,keywords = '一带一路',limit=800,taskId = 3,*args,**kwargs):
        super(LesoSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        # keywords = 'hello'
        self.limit_time = limit
        self.task_id = taskId
        self.site_name = '乐视网'
        self.info ='无简介'
        self.video_category = '未分类'
        self.allowed_domains = ['www.leso.cn','search.lekan.letv.com/apisearch_json.so']
        self.url1 = 'http://search.lekan.letv.com/lekan/apisearch_json.so?from=pc&' \
                    'wd='+self.keywords+'query='+self.keywords+'&pn='
        # url1 = 'http://www.soku.com/search_video/q_hello?site=14&page='
        self.page = 1
        self.start_urls = [self.url1+'2']
        # start_urls = ['http://www.soku.com/search_video/q_hello?site=14&page=1']

        # print('正在爬去第1页' )
    def parse(self, response):
        # print(response.text)
        video_list = json.loads(response.text)['video_list']
        # print(video_list[0])
        # item = LesospiderItem()
        for video in video_list:
            print(video.keys())