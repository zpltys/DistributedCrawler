# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from DistributedCrawler.items import DistributedCrawlerItem
#from urllib2 import Request
import urllib2
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup

class LinkSpider(RedisSpider):
    name = "linkspider"
    allowed_domains = ["taobao.com","tmall.com"]
    start_urls = ['http://www.taobao.com/']
    redis_key = 'linkspider:start_urls'

    def parse(self, response):
        #,'女鞋','男装'，'男鞋','运动','户外','数码','日用'
        keys = ['女装','女鞋','男装','男鞋','运动','户外','数码','日用']
        for i in keys:
            for j in range(1,20):
                #print(i)
                url = "https://s.taobao.com/search?q=" + i + "&ie=utf8&s=" + str((j - 1) * 44)
                #print("要爬取的url是:" + url)
                yield Request(url=url,callback=self.goodlist)

    def goodlist(self,response):
        body = response.body
        pat = '"nid":"(.*?)"'
        allid = re.compile(pattern=pat).findall(body)
        for id in allid:
            url = "https://item.taobao.com/item.htm?id=" + str(id)
            yield Request(url=url,callback=self.good,meta={"id":id})

    def good(self,response):
        id = response.meta["id"]
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
