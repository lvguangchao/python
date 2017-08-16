# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cName = scrapy.Field()
    eName=scrapy.Field()
    address = scrapy.Field()
    imgUrl = scrapy.Field()
    score = scrapy.Field()
    description = scrapy.Field()
    httpUrl=scrapy.Field()
    coordinate=scrapy.Field()
    top_amenities=scrapy.Field()
    hotel_amenities =scrapy.Field()
    room_amenities =scrapy.Field()
    things_to_do =scrapy.Field()
    room_types =scrapy.Field()
    location =scrapy.Field()
    number_of_rooms =scrapy.Field()
    code =scrapy.Field()
    reservation_options =scrapy.Field()
    tel =scrapy.Field()
    hotel_level =scrapy.Field()
    gCode =scrapy.Field()


