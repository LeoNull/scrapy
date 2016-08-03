# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy
from scrapy.loader import ItemLoader, Identity
from fun.items import MeizituItem


class MeizituSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com"]
    start_urls = (
        'http://www.meizitu.com/a/list_1_4.html',
    )

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath("//div[@id='maincontent']/div[@class='inWrap']/ul[@class='wp-list clearfix']/li[@class='wp-item']/div[@class='con']/div[@class='pic']/a/@href").extract():
            
            request = scrapy.Request(link, callback=self.parse_item)
            yield request
        #在首页审查元素时，获取页码集合
        pages = sel.xpath("//div[@class='navigation']/div[@id='wp_page_numbers']/ul/li/a/@href").extract()
        #如果得到的页码集合大于2，进入到倒数第二页抓取图片
        if len(pages) > 2:
            page_link = pages[8]
            print page_link
            page_link = page_link.replace('/a/', '')
            request = scrapy.Request('http://www.meizitu.com/a/%s' % page_link, callback=self.parse)
            yield request

    def parse_item(self, response):
        l = ItemLoader(item=MeizituItem(), response=response)
        l.add_xpath('name', '//h2/a/text()')
        l.add_xpath('tags', "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p")
        l.add_xpath('image_urls', "//div[@id='picture']/p/img/@src", Identity())
        l.add_value('url', response.url)
        return l.load_item()
