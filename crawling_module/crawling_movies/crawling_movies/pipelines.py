# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
import logging
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
import json
import pika


class MovieListPipeline:

    def open_spider(self, spider):
        self.file = open("../../movie_data/movie_list.jsonl", "wb")
        self.exporter = JsonLinesItemExporter(self.file)  # TODO bug here
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


# myproject/pipelines.py
class PipePipeline:
    def __init__(self, pipe_end):
        self.pipe_end = pipe_end

    @classmethod
    def from_crawler(cls, crawler):
        # Access the spider
        spider = crawler.spider
        pipe_end = getattr(spider, "pipe_end", None)
        return cls(pipe_end)

    def process_item(self, item, spider):
        self.pipe_end.send(item)  # Send item through the pipe
        return item

    def close_spider(self, spider):
        self.pipe_end.send("END")  # Send end signal
        self.pipe_end.close()  # Close the pipe end


class RabbitMQPipeline:

    def __init__(self, rabbitmq_connection, rabbitmq_queue):
        self.rabbitmq_connection = rabbitmq_connection
        self.rabbitmq_queue = rabbitmq_queue
        self.channel = self.rabbitmq_connection.channel()

    def send_message(self, exchange, queue, message):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange=exchange, routing_key=queue, body=message)

    @classmethod
    def from_crawler(cls, crawler):
        # Access the spider
        spider = crawler.spider
        rabbitmq_connection = getattr(spider, "rabbitmq_connection", None)
        rabbitmq_queue = getattr(spider, "rabbitmq_queue", None)
        return cls(rabbitmq_connection, rabbitmq_queue)

    def process_item(self, item, spider):
        # Publish the item to RabbitMQ
        message = json.dumps(ItemAdapter(item).asdict())
        self.send_message(exchange="", queue=self.rabbitmq_queue, message=message)

    def close_spider(self, spider):
        self.channel.close()