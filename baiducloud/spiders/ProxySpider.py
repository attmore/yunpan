# -*- coding: utf-8 -*-
__author__ = 'bobhu'

import scrapy
from scrapy.spiders import Spider
from baiducloud.items import ProxyItem
from scrapy import log

class ProxySpider(Spider):
    name = 'proxy'
    allowed_domains = ['http://www.xicidaili.com/']
    proxy_url_list = 'http://www.xicidaili.com/nn/{page_num}'

    def start_requests(self):
        # get top 10 page
        return [scrapy.FormRequest(self.proxy_url_list.format(page_num=page), callback=self.parse) for page in
                range(1, 2)]

    def parse(self, response):
        #
        proxy_list = response.xpath('//table[@id="ip_list"]/tr')

        for proxy in proxy_list[1:]:
            # pre_item = ProxyItem()
            # pre_item['ip'] = proxy.xpath('td[2]/text()')[0].extract()#取文字
            # pre_item['port'] = proxy.xpath('td[3]/text()')[0].extract()#取文字
            # pre_item['position'] = proxy.xpath('string(td[4]/a)')[0].extract().strip()
            # pre_item['type'] = proxy.xpath('td[6]/text()')[0].extract()
            # #speed取到td的title属性，再用正则（匹配到数字）
            # pre_item['speed'] = proxy.xpath('td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            # pre_item['last_check_time'] = proxy.xpath('td[10]/text()')[0].extract()
            log.msg('proxy')
            yield ProxyItem(ip=proxy.xpath('td[2]/text()')[0].extract(),
                            port=proxy.xpath('td[3]/text()')[0].extract(),
                            position=proxy.xpath('string(td[4]/a)')[0].extract(),
                            type=proxy.xpath('td[6]/text()')[0].extract(),
                            speed=proxy.xpath('td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0],
                            last_check_time=proxy.xpath('td[10]/text()')[0].extract())