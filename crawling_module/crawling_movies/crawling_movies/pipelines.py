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
        self.file = open('../../movie_data/movie_list.jsonl', 'wb')
        self.exporter = JsonLinesItemExporter(self.file) # TODO bug here
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


# pipelines.py
import sqlite3
from twisted.enterprise import adbapi

# myproject/pipelines.py
class PipePipeline:
    def __init__(self, pipe_end):
        self.pipe_end = pipe_end

    @classmethod
    def from_crawler(cls, crawler):
        # Get the pipe_end from the spider
        pipe_end = crawler.crawler.engine.spider.pipe_end
        return cls(pipe_end)

    def process_item(self, item, spider):
        self.pipe_end.send(item)  # Send item through the pipe
        return item

    def close_spider(self, spider):
        self.pipe_end.send("END")  # Send end signal
        self.pipe_end.close()  # Close the pipe end


        



class RabbitMQPipeline:
    def __init__(self) -> None:
        self._load_settings()
        self.connection = None
        self.channel = None

    def _load_settings(self) -> None:
        try:
            with open("../../settings/settings.json", mode="r") as f:
                settings = json.load(f)
                self.messaging_host = settings["crawling"]["messaging"]["RABBITMQ_HOST"]
                self.messaging_queue = settings["crawling"]["messaging"]["RABBITMQ_QUEUE"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load settings: {e}")
            raise

    def open_spider(self, spider) -> None:
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.messaging_host, port=5672)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.messaging_queue)
            logging.info(f"Connected to RabbitMQ at {self.messaging_host}, queue declared: {self.messaging_queue}")
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def close_spider(self, spider) -> None:
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
                logging.info("Connection to RabbitMQ closed.")
            except Exception as e:
                logging.error(f"Failed to close RabbitMQ connection: {e}")

    def process_item(self, item, spider) -> dict:
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.messaging_queue,
                body=json.dumps(dict(item), indent=4)
            )
            logging.info(f"Item sent to queue: {item}, routing key: {self.messaging_queue}, host: {self.messaging_host}")
        except Exception as e:
            logging.error(f"Failed to publish item to RabbitMQ: {e}")
        return item