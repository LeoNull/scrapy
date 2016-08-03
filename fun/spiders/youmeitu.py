# -*- coding: utf-8 -*-

from scrapy.selector import Selector
import scrapy
from scrapy.loader import ItemLoader, Identity
from fun.items import YoumeituItem

class YoumeituSpider(scrapy.Spider):
    name = "youmeitu"
    allowed_domains = ["www.topit.me/"]
    start_urls = (
        'http://www.topit.me/',
    )
    def parse(self,response):
        sel=Selector(response)
        for link in sel.xpath("//div[@class='catelog']/div[@class='e m']/a/@href").extract():
            print link
            request = scrapy.Request(link, callback=self.parse_item)
            yield request
        pages = sel.xpath("//div[@id='pagination']/div[@class='pages']/a[@id='page-next']/@href").extract()
        print len(pages)
        if len(pages) > 0:
            page_link = pages[2]
            request = scrapy.Request(page_link, callback=self.parse)
            yield request
            
    def parse_item(self,response):
        l = ItemLoader(item=YoumeituItem(), response=response)
        l.add_xpath('name', '//h2/a/text()')
        l.add_xpath('tags', "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p")
        l.add_xpath('image_urls', "//div[@id='mainbox']/div[@id='canvasbox']/div[@id='content']/a[@id='item-tip']/img/@src", Identity())
        l.add_value('url', response.url)
        return l.load_item()
        