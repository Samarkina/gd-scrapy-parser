# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    """Item for Article

    """
    title = scrapy.Field()
    url = scrapy.Field()
    firstSymbols = scrapy.Field()
    date = scrapy.Field()
    authorName = scrapy.Field()
    tags = scrapy.Field()


class AuthorItem(scrapy.Item):
    """Item for Author

    """
    name = scrapy.Field()
    jobTitle = scrapy.Field()
    linkedIn = scrapy.Field()
    counterArticles = scrapy.Field()
