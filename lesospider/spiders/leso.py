# -*- coding: utf-8 -*-
import json
import time
import scrapy
import re
import stat
from lesospider.items import LesospiderItem


class LesoSpider(scrapy.Spider):
    name = '关键词采集'

    def __init__(self, keywords='一带一路', video_time_long=600, video_time_short=0, task_id=2, startDate=int(time.time()) - 3600 * 48 * 87,
                 endDate=int(time.time()), *args, **kwargs):
        super(LesoSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        # keywords = 'hello'
        self.video_time_long = video_time_long
        self.video_time_short = video_time_short
        self.upload_time_start_date = startDate
        self.upload_time_end_date = endDate
        self.task_id = task_id
        self.site_name = '乐视网'
        self.info = '无简介'
        self.video_category = '未分类'
        self.allowed_domains = ['www.leso.cn', 'search.lekan.letv.com', 'www.le.com']
        self.url1 = 'http://search.lekan.letv.com/lekan/apisearch_json.so?from=pc&jf=1&hl=1&dt=1,2&ph=420001,420002&' \
                    'show=4&ps=35&wd=' + self.keywords + '&lc=d6e77564c06b615ab16616b24d3e2fbf&_=1526536864900&pn='

        self.page = 1
        self.start_urls = [self.url1 + '1']

        # print('正在爬去第1页' )

    def parse(self, response):
        video_list = json.loads(response.text)['data_list']
        item = LesospiderItem()
        item['video_time_long'] = self.video_time_long
        item['video_time_short'] = self.video_time_short
        item['start_date'] = self.upload_time_start_date
        item['end_date'] = self.upload_time_end_date
        for video in video_list:

            item['tags'] = []
            item['site_name'] = video.get('source', '乐视网')
            if item['site_name'] != 'letv':
                item['url'] = video.get('url')
            else:
                item['url'] = 'http://www.le.com/ptv/vplay/' + video['vid'] + '.html'
            print(item['url'])
            item['keywords'] = self.keywords
            item['task_id'] = self.task_id
            item['video_category'] = video.get('categoryName', '')
            item['title'] = self.translation(video.get('name', '')).strip()  # 视频标题
            item['play_count'] = video.get('playCount', '')
            item['info'] = video.get('description', '')
            item['video_time'] = video.get('duration', '')
            time1 = video.get('releaseDate', '')
            if time1 != '':
                item['upload_time'] = int(time1[:10])
            else:
                item['upload_time'] = self.start_date

            yield item

        self.page += 1
        if self.page <= 5:
            print("开始爬去第%d页" % self.page)
            url = self.url1 + str(self.page)
            time.sleep(5)
            # 再次发送请求
            yield scrapy.Request(url=url, callback=self.parse)

    def translation(self, instring):
        '''去掉数据中的空格换行等字符'''
        move = dict.fromkeys((ord(c) for c in u"\u0001\u0002\xa0\n\t|│:：<>？?\\/*’‘“”\""))
        outstring = instring.translate(move)
        return outstring

    def close(self, spider):
        # 当爬虫退出的时候 关闭chrome
        import datetime
        import os
        from scrapy.utils.project import get_project_settings

        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        settings = get_project_settings()
        videos_save_dir = settings['VIDEOS_SAVE_DIR']
        path = os.getcwd()  # 获取当前路径
        count = 0
        sizes = 0
        for root, dirs, files in os.walk(path + "/" + videos_save_dir + "/" + self.keywords.replace(' ', '_') + "/" + dt):  # 遍历统计
            for each in files:
                size = os.path.getsize(os.path.join(root, each))  # 获取文件大小
                os.chmod(os.path.join(root, each), stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
                sizes += size
                count += 1  # 统计文件夹下文件个数
        count = count // 2
        sizes = sizes / 1024.0 / 1024.0
        sizes = round(sizes, 2)
        videojson = {}
        videojson['title'] = self.keywords
        videojson['time'] = dt
        videojson['keywords'] = self.keywords
        videojson['file_number'] = count
        videojson['file_size'] = str(sizes) + 'M'
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        videojson = json.dumps(videojson, ensure_ascii=False)
        with open(videos_save_dir + '/' + self.keywords.replace(' ', '_') + "/" + dt + "/" + "task_info.json",
                  'w', encoding='utf-8') as fq:
            fq.write(videojson)
        os.chmod(videos_save_dir + '/' + self.keywords.replace(' ', '_') + "/" + dt + "/" + "task_info.json",
                 stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
        os.chmod(videos_save_dir + '/' + self.keywords.replace(' ', '_') + "/" + dt,
                 stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
        os.chmod(videos_save_dir + '/' + self.keywords.replace(' ', '_'),
                 stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
        os.chmod(videos_save_dir,
                 stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)
        print("spider closed")
