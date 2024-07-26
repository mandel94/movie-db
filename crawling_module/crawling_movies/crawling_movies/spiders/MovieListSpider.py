import scrapy
import re
import uuid
from thefuzz import fuzz
from typing import Literal
from urllib.parse import urlparse, urlunparse
from scrapy.loader import ItemLoader
from crawling_movies.items import MovieList
from crawling_movies.loaders import MovieListLoader
import requests

# Constants
JW_MOVIE_LIST_BASE_URL = "https://www.justwatch.com/us/provider/max/movies?page="
_JW_BASE_URL = "https://www.justwatch.com/"
_LOGS_PATH = "../../../logs/"
WIKI_CLIENT_ENDPOINTS = {
    "search_movies": "http://wiki_api_service:5000/v1/search/movies"
}

class MovieListSpider(scrapy.Spider):
    """
    Spider to scrape movie listings from JustWatch and match them with Wikipedia entries.

    Attributes:
        name (str): The name of the spider.
        custom_settings (dict): Custom settings for the spider, including download delay and pipelines.
        page_limit (int): The maximum number of pages to scrape.
        start_urls (list): The initial URLs to start scraping from.
    """
    name = "get_movie_list_from_justwatch"

    custom_settings = {
        "DOWNLOAD_DELAY": 0.4,
        "ITEM_PIPELINES": {
            "crawling_movies.pipelines.MovieListPipeline": 300,
            "crawling_movies.pipelines.PipePipeline": 500,
        },
        "LOG_LEVEL": "ERROR"
    }

    page_limit = 1
    start_urls = [f"{JW_MOVIE_LIST_BASE_URL}1"]

    def __init__(self, pipe_end=None, *args, **kwargs):
        """
        Initialize the spider.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.pipe_end = pipe_end
        self.page_nb = 1

    def parse(self, response):
        """
        Parse the response from JustWatch and extract movie data.

        Args:
            response (scrapy.http.Response): The response object from JustWatch.
        """
        movie_cards = response.css("div[data-id]")
        if not movie_cards:
            self.logger.warning("No movie cards found on the page.")

        for movie in movie_cards:
            yield self.parse_movie(movie, response)

        if self.has_next_page():
            self.page_nb += 1
            yield scrapy.Request(url=self.construct_page_url(self.page_nb), callback=self.parse)

    def parse_movie(self, movie, response):
        """
        Parse individual movie data from a movie card.

        Args:
            movie (scrapy.selector.Selector): The movie card selector.
            response (scrapy.http.Response): The response object from JustWatch.

        Returns:
            dict: The loaded movie item.
        """
        loader = MovieListLoader(item=MovieList(), response=response)
        movie_id = self.generate_uuid()
        title = self.extract_title(movie)

        if not title:
            self.logger.warning("Title not found.")
            return

        jw_href = self.get_justwatch_href(movie)
        if not jw_href:
            self.logger.warning(f"Justwatch href not found for {title}")
            return

        wiki_match = self.match_with_wiki(title)
        loader.add_value("movie_list_id", movie_id)
        loader.add_value("title", title)
        loader.add_value("wiki_href", wiki_match.get("url", ""))
        loader.add_value("jw_href", self.construct_jw_url(jw_href))

        return loader.load_item()

    def get_justwatch_href(self, movie):
        """
        Extract the JustWatch href from a movie card.

        Args:
            movie (scrapy.selector.Selector): The movie card selector.

        Returns:
            str: The JustWatch href.
        """
        href = movie.xpath("a[@class='title-list-grid__item--link']/@href").get()
        return href[1:] if href and href.startswith("/") else href

    def has_next_page(self):
        """
        Check if there are more pages to scrape.

        Returns:
            bool: True if there are more pages, False otherwise.
        """
        return self.page_nb < self.page_limit

    def construct_page_url(self, page_nb):
        """
        Construct the URL for the next page.

        Args:
            page_nb (int): The page number.

        Returns:
            str: The URL for the next page.
        """
        return f"{JW_MOVIE_LIST_BASE_URL}{page_nb}"

    def construct_jw_url(self, href):
        """
        Construct the full JustWatch URL.

        Args:
            href (str): The href extracted from the movie card.

        Returns:
            str: The full JustWatch URL.
        """
        return f"{_JW_BASE_URL}{href}"

    def generate_uuid(self):
        """
        Generate a unique identifier for each movie.

        Returns:
            str: A UUID string.
        """
        return str(uuid.uuid4())

    def extract_title(self, movie):
        """
        Extract the movie title from a movie card.

        Args:
            movie (scrapy.selector.Selector): The movie card selector.

        Returns:
            str: The movie title.
        """
        return movie.xpath("@data-title").get()

    def match_with_wiki(self, movie_title: str) -> dict:
        """
        Match the movie title with a Wikipedia entry.

        Args:
            movie_title (str): The title of the movie.

        Returns:
            dict: The matched Wikipedia entry, or None if no match is found.
        """
        wiki_results = requests.get(
            WIKI_CLIENT_ENDPOINTS["search_movies"],
            params={"title": movie_title},
        )

        self.log_wiki_results(wiki_results)

        if wiki_results.status_code == 404 or wiki_results.json().get("how_many") == 0:
            self.logger.info(f"No match found for {movie_title}")
            return {"url": None}

        return self.best_fuzzy_match(movie_title, wiki_results.json())

    def best_fuzzy_match(self, movie_title: str, wiki_results: dict) -> dict:
        """
        Find the best fuzzy match for the movie title in the Wikipedia results.

        Args:
            movie_title (str): The title of the movie.
            wiki_results (dict): The results from the Wikipedia API.

        Returns:
            dict: The best matched Wikipedia entry, or None if no match is found.
        """
        similarity_scores = {
            movie["key"]: self.compute_string_similarity(movie_title, movie["key"])
            for movie in wiki_results.get("movies", [])
        }
        best_match = max(similarity_scores, key=similarity_scores.get, default=None)
        return next((movie for movie in wiki_results.get("movies", []) if movie["key"] == best_match), {"url": None})

    def compute_string_similarity(self, str1: str, str2: str, method: Literal["simple", "partial", "token_sort_ratio"] = "simple") -> int:
        """
        Compute the similarity score between two strings.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.
            method (Literal): The method to use for computing similarity.

        Returns:
            int: The similarity score.
        """
        if method == "simple":
            return fuzz.ratio(str1, str2)
        elif method == "partial":
            return fuzz.partial_ratio(str1, str2)
        elif method == "token_sort_ratio":
            return fuzz.token_sort_ratio(str1, str2)

    def log_wiki_results(self, wiki_results):
        """
        Log the Wikipedia results to a file.

        Args:
            wiki_results (requests.Response): The response from the Wikipedia API.
        """
        with open(_LOGS_PATH + "temp.log", mode="a") as f:
            f.write(f"Wiki results: {wiki_results.json()}\n")

def remove_special_characters(string: str):
    """
    Remove special characters from a string.

    Args:
        string (str): The input string.

    Returns:
        str: The cleaned string with special characters removed.
    """
    return re.sub(r"[^a-zA-Z0-9]+", " ", string)
