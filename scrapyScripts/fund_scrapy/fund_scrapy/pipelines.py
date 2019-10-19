# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Mongo_Client import Mongo_Client
import pika
import json


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


class FundRabblitMQPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):

        credentials = pika.PlainCredentials('raycdut', 'abc@1234')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.3.18', credentials=credentials))
        # 创建频道
        channel = connection.channel()
        # 创建一个队列名叫hello
        channel.queue_declare(queue='fundlist')
        # exchange -- 它使我们能够确切地指定消息应该到哪个队列去。
        # 向队列插入数值 routing_key是队列名 body是要插入的内容
        channel.basic_publish(exchange='',
                              routing_key='fundlist',
                              body=json.dumps(item._values))

        print("开始队列")
        # 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
        connection.close()
