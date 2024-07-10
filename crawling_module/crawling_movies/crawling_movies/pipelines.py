# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter


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
