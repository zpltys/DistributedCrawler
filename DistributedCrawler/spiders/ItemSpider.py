#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scrapy
import redis
from bs4 import BeautifulSoup
from DistributedCrawler.items import DistributedCrawlerItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import re

class ItemSpider(RedisSpider):
    name = "itemspider"
    redis_key = "test:urls"
    allowed_domains = ["taobao.com","tmall.com"]
    #start_urls=['https://item.taobao.com/item.htm?spm=a21bo.7929913.198967.23.1xhCP0&id=544532352320']

    def parse(self, response):
        source='taobao'
        try:
            soup=BeautifulSoup(response.body,'html5lib')
        except:
            print('Explaination Error!')
            return
            
        try:
            content = soup.find('h3',{'class':'tb-main-title'})
            product_name=content['data-title']
        except:
            #title = response.xpath("//h1[@data-spm='1000983']/text()").extract()[0]
            source='tianmao'
            namelist = soup.find('h1',{'data-spm':'1000983'}).string
            product_name=""
            for i in namelist:
                product_name += i+' '
        try:
            content = soup.find('div',{'class':'tb-shop-rate'}).find_all('dl')
            rank=0
            for i in content:
                rank+=float((i.dd.a.string.split())[0])
            rank=round(rank/3,2)
        except:
            content = soup.find_all('span',{'class':'shopdsr-score-con'})
            rank=0
            for i in content:
                print(float(i.string))
                rank+=float(i.string)
            rank=round(rank/3,2)

        try:
            content = soup.find('div',{'class':'tb-shop-name'}).find('a') 
            namelist=content.string.split()
            store_name=""
            for i in namelist:
                store_name += i+' '
        except:
            content = soup.find('a',{'class':'slogo-shopname'}) 
            namelist=content.string.split()
            store_name=""
            for i in namelist:
                store_name += i+' '
                

        item = DistributedCrawlerItem()
        item['rank'] = rank
        item['product'] = product_name
        item['store'] = store_name
        item['resource']=source
        yield item


        
    
