#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scrapy
import redis
from bs4 import BeautifulSoup
from DistributedCrawler.items import DistributedCrawlerItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import re

class UrlSpider(scrapy.Spider):
    name = "urlspider"
    allowed_domains = ["taobao.com","tmall.com"]
    start_urls=['https://www.taobao.com']
    def parse(self, response):
        keys = ['女装','女鞋','男装','男鞋','运动','户外','数码','日用']
        for i in keys:
            for j in range(1,20):  #j是每类商品要爬的页数
                #print(i)
                url = "https://s.taobao.com/search?q=" + i + "&ie=utf8&s=" + str((j - 1) * 44)
                #print("要爬取的url是:" + url)
                yield Request(url=url,callback=self.goodlist)

    def goodlist(self,response):
        body = response.body
        r=redis.Redis(host='localhost',port=6379)
        pat = '"nid":"(.*?)"'
        allid = re.compile(pattern=pat).findall(body)
        for id in allid:
            url = "https://item.taobao.com/item.htm?id=" + str(id)
            r.lpush('test:urls',url)
            #yield Request(url=url,callback=self.parse)



