# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Mongo_Client import Mongo_Client


class FundScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class FundPostgrePipeline(object):
    def process_item(self, item, spider):

        return item


class FundMongoPipeline(object):
    def __init__(self):
        self.client = Mongo_Client()
        self.fund = self.client.db['Fund']

    def process_item(self, item, spider):
        self.fund.insert_one(dict(item))
        return item
