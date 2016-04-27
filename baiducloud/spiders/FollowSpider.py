# -*- coding: utf-8 -*-
__author__ = 'bobhu'

import re

import scrapy
from scrapy.spiders import Spider
from scrapy import log
from baiducloud.items import UserItem
from baiducloud import db


class FollowSpider(Spider):
    name = 'follow'
    allowed_domains = ['yun.baidu.com']
    wap_follow_url = 'http://yun.baidu.com/wap/share/home/followers?uk={uk}&third=0&start={start}'

    def start_requests(self):
        count = db.get('select count(*) as count from bc_user')['count']
        if count:
            log.msg('count > 0')
            return [scrapy.FormRequest(self.wap_follow_url.format(uk=row['uk'], start=0), callback=self.parse)
                    #get user not crawled share
                    for row in db.query('select * from bc_user where follow_crawled = 0 limit 1000')]
        else:
            log.msg('count == 0 ,default')
            return [scrapy.FormRequest(self.wap_follow_url.format(uk=3409247005, start=0), callback=self.parse)]

    def parse(self, response):
        uk = re.findall(r'uk=(\d+)', response.request.url)[0]
        follower_total_count = int(re.findall(r"totalCount:\"(\d+)\"", response.body)[0])
        #set follow_crawled flag
        db.update('update bc_user set follow_crawled=1 where uk=%s', uk)

        if follower_total_count > 0:
            urls = [self.wap_follow_url.format(uk=uk, start=start) for start in range(20, follower_total_count, 20)]

            for url in urls:
                yield scrapy.Request(url, callback=self.parse_follow)

            follow_uk_list = re.findall(r"follow_uk\\\":(\d+)", response.body)

            for uk in follow_uk_list:
                yield UserItem(uk=uk)
                yield scrapy.Request(self.wap_follow_url.format(uk=uk, start=0), callback=self.parse)

    def parse_follow(self, response):
        uk = re.findall(r'uk=(\d+)', response.request.url)[0]

        follow_uk_list = re.findall(r"follow_uk\\\":(\d+)", response.body)

        for uk in follow_uk_list:
            yield UserItem(uk=uk)
            yield scrapy.Request(self.wap_follow_url.format(uk=uk, start=0), callback=self.parse)
