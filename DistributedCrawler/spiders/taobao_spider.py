#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scrapy
import redis
from bs4 import BeautifulSoup
from DistributedCrawler.items import DistributedCrawlerItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import re

class DmozSpider(RedisSpider):
    name = "taobao"
    redis_key = "dmozspider:start_urls"
    allowed_domains = ["taobao.com"]
    #start_urls=['https://item.taobao.com/item.htm?spm=a21bo.7929913.198967.23.1xhCP0&id=544532352320']

    def parse(self, response):
        #body=response.body
        #f=open('d.txt','wb')
        #f.write(response.body)
        #f.close()
        #pat='"nid":"(.*?)",'
        #allid=re.compile(pattern=pat).findall(body)
        #for id in allid:
         #   print(str(id))

        #new url
        soup=BeautifulSoup(response.body,'html5lib')
        content=soup.find_all('a')
        #print('fsdfd')
        f=open('d.txt','wb')
        for a in content:
            url=a['href']
            f.write(url)
        f.close()
            #if url.find('item.taobao.com')!=-1:
            #    yield Request(url, callback='parse_url')

    def parse_url(self, response):
        soup=BeautifulSoup(response.body,'html5lib')
        try:
            #print("url:%s"% response.url)

            #comment
            content = soup.find('div',{'class':'tb-shop-rate'}).find_all('dl')
            rank=0
            for i in content:
                rank+=float((i.dd.a.string.split())[0])
            rank=round(rank/3,2)

            #product name
            content = soup.find('h3',{'class':'tb-main-title'})
            product_name=content['data-title']
            #print(product_name)

            #store name
            content = soup.find('div',{'class':'tb-shop-name'}).find('a')
            namelist=content.string.split()
            store_name=""
            for i in namelist:
                store_name += i+' '
            #print(store_name)

            item=DistributedCrawlerItem()
            item['rank'] = rank
            item['product'] = product_name
            item['store'] = store_name
            item['resource']='taobao'

            yield item
        except:
            pass
        #  yield Request(url, callback='parse')
