from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl("get_movie_list_from_justwatch")
    process.start()


if __name__ == "__main__":
    run_spiders()







