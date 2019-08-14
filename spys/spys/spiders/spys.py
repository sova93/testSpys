# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from spys.items import SpysItemLoader, SpysItem
from scrapy import Request

class SpysSpider(scrapy.Spider):
    name = 'spys'
    allowed_domains = ['spys.one']

    def start_requests(self):
        yield SplashRequest(
            url='http://spys.one/proxies/',
            callback=self.parse,
        )

    def parse_func(self, response):
        for tr in response.css('tr[onmouseout]'):
            tr_el = tr.css('td font::text')
            l = SpysItemLoader(SpysItem(), tr)
            for td in range(len(tr_el)):
                if td == 1:
                    l.add_value('address',tr_el[td].extract())
                if td == 3:
                    l.add_value('port', tr_el[td].extract())
            yield l.load_item()

    def parse(self, response):
        str_list= []
        for el in response.css('font.spy3::text').extract():
            if el.isdigit():
                str_list.append(int(el))
        count_str = max(str_list)
        for next_page_n in reversed(range(count_str + 1)):
            if next_page_n > 0:
                next_page_url = response.urljoin(str(next_page_n))
                yield SplashRequest(url=next_page_url, callback=self.parse_func)
