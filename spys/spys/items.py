import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join


class SpysItem(scrapy.Item):
    address = scrapy.Field()
    port = scrapy.Field()


class SpysItemLoader(ItemLoader):
    address_out = TakeFirst()
    port_out = TakeFirst()
