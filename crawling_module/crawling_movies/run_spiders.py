import multiprocessing
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater
from scrapy.utils.log import configure_logging
import logging
from utils import create_rabbitmq_connection, _load_settings


def get_movie_list(pipe_end):
    crawler_settings = get_project_settings()
    configure_logging()
    runner = CrawlerRunner(crawler_settings)
    d = runner.crawl("get_movie_list_from_justwatch", pipe_end=pipe_end)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # Block until the crawling is finished


def scrape_movie_item(pipe_end, rabbitmq_connection, rabbitmq_queue):
    crawler_settings = get_project_settings()
    configure_logging()
    runner = CrawlerRunner(crawler_settings)

    def _crawl():
        item_info = pipe_end.recv()
        logging.error(f"Received item info: {item_info}")
        if item_info == "END":  # End of pipeline
            reactor.stop()
        else:
            d = runner.crawl(
                "scrape_movie",
                item_info=item_info,
                rabbitmq_connection=rabbitmq_connection,
                rabbitmq_queue=rabbitmq_queue,
            )
            d.addBoth(lambda _: deferLater(reactor, 0, _crawl))

    _crawl()
    reactor.run()


if __name__ == "__main__":
    rabbitmq_settings = (
        _load_settings()
    )  # Load rabbit settings from shared settings volume

    rabbitmq_connection = create_rabbitmq_connection(
        rabbitmq_settings["RABBITMQ_HOST"],
        rabbitmq_settings["RABBITMQ_PORT"],
        rabbitmq_settings["RABBITMQ_USER"],
        rabbitmq_settings["RABBITMQ_PASSWORD"],
    )

    parent_conn, child_conn = multiprocessing.Pipe()

    # Start Scrapy in a separate process
    movie_list_process = multiprocessing.Process(
        target=get_movie_list, args=(child_conn,)
    )
    movie_list_process.start()

    # Create second process that handles movie data and creates movie items
    movie_process = multiprocessing.Process(
        target=scrape_movie_item,
        args=(
            parent_conn,
            rabbitmq_connection,
            rabbitmq_settings["MOVIES"]["QUEUE"],
            rabbitmq_settings["MOVIES"]["EXCHANGE"],
        ),
    )
    movie_process.start()

    movie_process.join()
    movie_list_process.join()

    # Close connections
    parent_conn.close()
    child_conn.close()
    rabbitmq_connection.close()
