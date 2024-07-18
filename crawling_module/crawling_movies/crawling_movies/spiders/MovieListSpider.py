import scrapy
import re
from scrapy.loader import ItemLoader
from crawling_movies.items import MovieList
from urllib.parse import urlparse, urlunparse
from crawling_movies.loaders import MovieListLoader
import requests
import uuid
from thefuzz import fuzz
from typing import Literal
from utils import spider_logs_file, write_on_file
import requests

jw_movie_list_base_url = "https://www.justwatch.com/us/provider/max/movies?page="
_jw_base_url = "https://www.justwatch.com/"
_jw_movies_base_url = _jw_base_url + "movies/"
wiki_client_endpoints = {
    "search_movies": "http://wiki_api_service:5000/v1/search/movies"
}

LOGS_PATH = "../../../logs/"


def remove_special_characters(string: str):
    """Remove special characters from a string"""
    # Remove special characters
    string = re.sub(r"[^a-zA-Z0-9]+", " ", string)
    return string



def _best_fuzzy_match(movie_title: str, wiki_results: dict) -> dict:
    """Returns the movie from wiki_results that matches the movie_title the best. If no match is found, returns None."""
    match_prop = "key"
    similarity_scores = {
        movie[match_prop]: _compute_string_similarity(movie_title, movie[match_prop])
        for movie in wiki_results[
            "movies"
        ]  # CONTRACT: The wiki client should return a json object with a 'movies' key, with a list of movies
    }
    best_match = max(similarity_scores, key=similarity_scores.get)
    for movie in wiki_results["movies"]:
        if movie[match_prop] == best_match:
            return movie


def _compute_string_similarity(
    str1: str,
    str2: str,
    method: Literal["simple", "partial", "token_sort_ratio"] = "simple",
) -> int:
    """Returns a similarity score between two strings."""
    if method == "simple":
        return fuzz.ratio(str1, str2)
    elif method == "partial":
        return fuzz.partial_ratio(str1, str2)
    elif method == "token_sort_ratio":
        return fuzz.token_sort_ratio(str1, str2)


def _match_with_wiki(movie_title: str) -> dict:
    wiki_results = requests.get(
        wiki_client_endpoints["search_movies"],
        params={"title": movie_title},
    )  # One (input title) to-many (output wiki results)
    # with open(LOGS_PATH+"temp.log", mode="a") as f:
    #     f.write(f"Wiki results = {wiki_results.json()}\n")
    with open(LOGS_PATH+"temp.log", mode="a") as f:
        f.write(f"Wiki results: {wiki_results}\n")
    # Get body of the response
    if wiki_results.status_code == 404:
        return {"url": None}
    # Check if wiki_results has an error key
    if wiki_results.json()["how_many"] == 0:
        write_on_file(spider_logs_file, f"No match found for {movie_title}\n")
        return {"url": None}
    return _best_fuzzy_match(movie_title, wiki_results.json())


class JustWatchMovieListSpider(scrapy.Spider):
    name = "get_movie_list_from_justwatch"

    page_limit = 3

    custom_settings = {"DOWNLOAD_DELAY": 0.4}

    start_urls = [jw_movie_list_base_url + "1"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "crawling_movies.pipelines.MovieListPipeline": 300,
        },
    }

    def __init__(self):
        self.page_nb = 1

    def parse(self, response):
        movie_cards = response.css("div[data-id]")
        for movie in movie_cards:
            loader = MovieListLoader(item=MovieList(), response=response)
            id_ = str(uuid.uuid4())
            title = movie.xpath("@data-title").get()
            # jw_href = _get_justwatch_href(title)
            jw_href = movie.xpath(
                "a[@class='title-list-grid__item--link']/@href" # It works by removing any leading slash
            ).get()[1:] # Remove leading slash
            with open(LOGS_PATH+"xpath.log", mode="a") as f:
                f.write(f"Justwatch href = {title}\n")
            wiki_match = _match_with_wiki(title)
            loader.add_value("movie_list_id", id_)
            loader.add_value("title", title)
            loader.add_value(
                "wiki_href", wiki_match["url"]
            )  # CONTRACT: The wiki client should return a json object with a 'url' key
            loader.add_value("jw_href", _jw_base_url+jw_href)
            yield loader.load_item()

        self.page_nb += 1
        if self.page_nb <= self.page_limit:
            next_page = jw_movie_list_base_url + str(self.page_nb)
            yield scrapy.Request(url=next_page, callback=self.parse)
