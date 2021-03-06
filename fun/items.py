# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class MeizituItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class CoserItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    info = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class YoumeituItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    info = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class MyItemLoader(ItemLoader):
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
