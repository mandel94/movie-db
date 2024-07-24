# from twisted.internet import reactor
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# import json


# def run_spiders():
#     process = CrawlerProcess(get_project_settings())
#     process.crawl("get_movie_list_from_justwatch") 
#     # process.crawl("scrape_movies")
#     process.start()


# if __name__ == "__main__":
#     with open("../settings/settings.json", mode="r") as f:
#         settings = json.load(f)
#         with open("../logs/temp.log", mode="a") as f:
#             f.write(f"Settings: {settings}\n")
#     run_spiders()

import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def get_movie_list(pipe_end):
    settings = get_project_settings()
    settings.set('ITEM_PIPELINES', {
        'myproject.pipelines.PipePipeline': 1,
    })
    process = CrawlerProcess(settings)
    process.crawl("get_movie_list_from_justwatch", pipe_end=pipe_end)
    process.start()


if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start Scrapy in a separate process
    movie_list_process = multiprocessing.Process(target=get_movie_list, args=(child_conn,))
    movie_list_process.start()

    # Create second process that handle movie data and creates movie items
    movie_process = multiprocessing.Process(target=scrape_movie_item, args=(parent_conn,))  
    movie_process.start() 
    movie_process.join()
    movie_list_process.join()

    # Close the connection
    parent_conn.close()
    child_conn.close()
