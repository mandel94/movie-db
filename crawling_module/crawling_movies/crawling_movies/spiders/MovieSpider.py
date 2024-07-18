import scrapy
from dotenv import load_dotenv

load_dotenv()


# Get the list of movies from the website

MOVIE_LIST_PATH = 'movie_list.jsonl' 

class MovieSpider(scrapy.Spider):
    name = 'scrape_movies'

    def __init__(self):
        pass
    
    # Make a request for each movie
    def start_requests(self):
        for movie in self.movies:
            yield scrapy.Request(movie.wiki_href, self.parse)
            

    # Parse the movie page
    def parse(self, response):
        pass