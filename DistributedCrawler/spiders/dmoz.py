from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from ..items import DistributedCrawlerItem

class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    start_urls = ['http://www.baidu.com/']

    def parse_directory(self, response):
        print "url:%s" % response.url
        print 'woq'

    def parse(self, response):
        print 'url:%s' % response.url
#        print response.text
        item = DistributedCrawlerItem()
        item['product'] = 'test_product'
        item['store'] = 'test_store'
        item['resource'] = 'taobao'
        item['rank'] = 0.5
        yield item
        print response.text
        urls = response.xpath("//body/div[@id='wrapper']/div[@id='head']/div[@class='head_wrapper']/div[@id='u1']/a").re("https?://.*\.com")
        for url in urls:
            yield Request(url, callback = 'parse_directory')
