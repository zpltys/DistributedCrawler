# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DistributedCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rank = scrapy.Field()     #得分(0-1)
    product = scrapy.Field()  #产品名称
    store = scrapy.Field()  #店铺

    resource = scrapy.Field() #来源，例如taobao
