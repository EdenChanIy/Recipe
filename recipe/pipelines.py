# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class RecipePipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open('test.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

#爬取图片
class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            if image_url:
                item['image_name'] = image_url.split('/')[-1]
                yield scrapy.Request(image_url)