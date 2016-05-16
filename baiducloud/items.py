# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    uk = scrapy.Field()


class ResourceItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    feed_time = scrapy.Field()
    feed_username = scrapy.Field()
    feed_user_uk = scrapy.Field()
    size = scrapy.Field()
    v_cnt = scrapy.Field()
    d_cnt = scrapy.Field()
    t_cnt = scrapy.Field()


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    position = scrapy.Field()
    type = scrapy.Field()
    speed = scrapy.Field()
    last_check_time = scrapy.Field()