# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentspiderItem(scrapy.Item):
    movie_comment_content = scrapy.Field()
    movie_comment_title = scrapy.Field()
    movie_name = scrapy.Field()


class MovieInfoItem(scrapy.Item):
    movie_name = scrapy.Field()
    director = scrapy.Field()
    actor_list = scrapy.Field()
    description = scrapy.Field()
    duration = scrapy.Field()
    category = scrapy.Field()
    date = scrapy.Field()
