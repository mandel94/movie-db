from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pika
import json


def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl("get_movie_list_from_justwatch") 
    # process.crawl("scrape_movies")
    process.start()


if __name__ == "__main__":
    with open("../settings/settings.json", mode="r") as f:
        settings = json.load(f)
        with open("../logs/temp.log", mode="a") as f:
            f.write(f"Settings: {settings}\n")
    run_spiders()







