import scrapy
from bs4 import BeautifulSoup
from DistributedCrawler.items import DistributedCrawlerItem
from scrapy_redis.spiders import CrawlSpider
from scrapy.http import Request

class DmozSpider(CrawlSpider):
    name = "taobao"
#    redis_key = "dmozspider:start_urls"
    allowed_domains = ["taobao.com"]
    start_urls=['https://detail.tmall.com/item.htm?spm=a1z10.4-b-s.w5003-16307040254.1.yFww02&id=548514707720&scene=taobao_shop']

    def parse(self, response):
        soup=BeautifulSoup(response.body,'html5lib')

        try:
            #comment
            content = soup.find('div',{'class':'tb-shop-rate'}).find_all('dl')
            rank=0
            for i in content:
                rank+=float((i.dd.a.string.split())[0])
                rank=round(rank/3,2)

            #product name
            content = soup.find('h3',{'class':'tb-main-title'})
            product_name=content.string.split()[0]
            #print(product_name)

            #store name
            content = soup.find('div',{'class':'tb-shop-name'}).find('a')
            store_name=content.string.split()[0]
            #print(store_name)

            item=DistributedCrawlerItem()
            item['rank'] = rank
            item['product'] = product_name
            item['store'] = store_name
            item['resource']='taobao'

            print 'zs-log: ' + str(item)
            yield item
        except:
            print "zs-log error parse item"
        print 'zs-log: efwef'

            #new url
        content=soup.find_all('a')
        for a in content:
            url=a['href']
            print "url:" + url
            try:
                r = Request(url, callback = 'parse')
                yield r
            except:
                pass
