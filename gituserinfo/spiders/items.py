# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Github_Item(scrapy.Item):
    fullname = scrapy.Field()
    username = scrapy.Field()
    location = scrapy.Field()
    repos = scrapy.Field()
    # organization = scrapy.Field()
    # mail = scrapy.Field()
    # joined = scrapy.Field()
    starred = scrapy.Field()
    followers = scrapy.Field()

    # following = scrapy.Field()

    # contribute = scrapy.Field()

    # repo_contributions = scrapy.Field()
    pass


class User_repo(scrapy.Item):
    username = scrapy.Field()
    java = scrapy.Field()

