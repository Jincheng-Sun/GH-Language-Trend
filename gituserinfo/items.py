# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GituserinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Github_Item(scrapy.Item):
    fullname = scrapy.Field()
    username = scrapy.Field()
    organization = scrapy.Field()
    mail = scrapy.Field()
    joined = scrapy.Field()
    followers = scrapy.Field()
    starred = scrapy.Field()
    following = scrapy.Field()
    popular_repos = scrapy.Field()
    repo_contributions = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
