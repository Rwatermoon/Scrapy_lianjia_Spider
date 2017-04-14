# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LjspiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    detials = scrapy.Field()
    location = scrapy.Field()
    total_price=scrapy.Field()
    single_price=scrapy.Field()
    claw_time=scrapy.Field()
    geo_location=scrapy.Field()
    pass
