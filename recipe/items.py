# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #食谱名字
    name = scrapy.Field()
    #食谱主要描述
    description = scrapy.Field()
    #难度
    difficulty = scrapy.Field()
    #时间
    time = scrapy.Field()
    #主料
    main_ingredient = scrapy.Field()
    #辅料
    minor_ingredient = scrapy.Field()
    #小贴士
    tips = scrapy.Field()
    #分类
    tags = scrapy.Field()
    #url
    url = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field() #存放图片名字
    pass
