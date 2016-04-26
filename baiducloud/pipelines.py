# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log

from baiducloud.items import UserItem, ResourceItem
from baiducloud import db


class UserPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            sql = 'insert into bc_user (uk, share_crawled, follow_crawled,follow_num) values ( %s, %s, %s,%s) ON DUPLICATE KEY UPDATE follow_num = follow_num + 1;'
            try:
                db.insert(sql, item['uk'], 0, 0, 0)
            except Exception as e:
                log.msg(e)
        return item


class ResourcePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ResourceItem):
            sql = ('insert into resource'
                   '(url, title, feed_time, feed_username, feed_user_uk, size, v_cnt, d_cnt, t_cnt)'
                   'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)')

            try:
                db.insert(sql,
                          item.get('url'),
                          item.get('title'),
                          item.get('feed_time'),
                          item.get('feed_username'),
                          item.get('feed_user_uk'),
                          item.get('size'),
                          item.get('v_cnt'),
                          item.get('d_cnt'),
                          item.get('t_cnt'))
            except Exception as e:
                log.msg(e)

        return item
