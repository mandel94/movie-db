# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
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



class RabbitMQPipeline:
    def __init__(self) -> None:
        with open("../../settings/settings.json", mode="r") as f: # Volume shared across containers
            settings = json.load(f)
            self.messaging_host = settings["crawling"]["messaging"]["RABBITMQ_HOST"]
            self.messaging_queue = settings["crawling"]["messaging"]["RABBITMQ_QUEUE"]

    def open_spider(self, spider):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.messaging_host,
                                      port=5672)
        )
        with open("../../logs/temp.log", mode="a") as f:
            f.write(f"Connection info:\n")
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.messaging_queue)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # self.channel.basic_publish(
        #     exchange='',
        #     routing_key=self.messaging_queue,
        #     body=json.dumps(dict(item))
        # )
        self.channel.basic_publish(
            exchange='',
            routing_key=self.messaging_queue,
            body=json.dumps(dict(item), indent=4)
        )
        with open("../../logs/temp.log", mode="a") as f:
            f.write(f"Item sent to queue: {item}\n"
                    f"with routing key: {self.messaging_queue}\n"
                    f"on host: {self.messaging_host}\n")
        return item
    

