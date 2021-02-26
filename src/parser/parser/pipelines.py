# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import vars as vars
from scrapy.exporters import JsonItemExporter


class GeneralPipeline(object):
    """Pipeline for writing to "filename" file
    """
    def __init__(self):
        self.filename = None

    def open_spider(self, spider):
        self.file = open(self.filename, 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class AuthorsPipeline(GeneralPipeline):
    """Pipeline for writing to FULL_FILENAME_TEMP_AUTH file
    """
    def __init__(self):
        super().__init__()
        self.filename = vars.FULL_FILENAME_TEMP_AUTH


class ArticlesPipeline(GeneralPipeline):
    """Pipeline for writing to FULL_FILENAME_TEMP_ART file
    """
    def __init__(self):
        super().__init__()
        self.filename = vars.FULL_FILENAME_TEMP_ART
