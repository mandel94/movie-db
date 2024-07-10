from dotenv import load_dotenv
import os
import requests
from exceptions import WikiSearchPageError, PageError, handle_error
import re
# from custom_logging import write_to_wiki_client_logs, write_to_wiki_client_error_logs
import datetime


load_dotenv()


BASE_URL = "https://api.wikimedia.org/core/v1/wikipedia/"
SEARCH_ENDPOINT = "/search/page"
LOGS_FOLDER = "../logs/"
LOGS_PATH = LOGS_FOLDER + "wiki_client.log"
ERROR_LOGS_PATH = LOGS_FOLDER + "wiki_client_errors.log"

MOVIE_RE_FLAGS = [
    "movie",
    "film[^s]",  # Matches a film but not a list of films
    "television series",
    "TV series",
    "tv_series",
    "television_series",
    "documentary",
    "miniseries",
    "animated",
    "series",
    "show",
    "episode",
    "season",
    "cinema",
    "filmography",
]


class WikiClient:
    """Create a client that connects to the WikiMedia API.

    For further information, please visit the WikiMedia API documentation:
    https://en.wikipedia.org/api/rest_v1/#/
    """

    def __init__(self, rate_limit: int, language_code: str = "en") -> None:
        self.headers = {"Authorization": "Bearer " + os.getenv("WIKI_API_TOKEN")}
        self.language_code = language_code
        self.base_url = BASE_URL + self.language_code
        self.article_base_url = f"https://{self.language_code}.wikipedia.org/wiki/"
        self.rate_limit = rate_limit

    def _return_url(self, page: dict) -> str:
        return self.article_base_url + page["key"]

    def search_page(self, search_query: str, nb_results: int = 1) -> dict:
        parameters = {"q": search_query, "limit": nb_results}
        response = requests.get(
            self.base_url + SEARCH_ENDPOINT,
            headers=self.headers,
            params=parameters,
            verify=False,
        )
        if response.status_code != 200:
            raise WikiSearchPageError(search_query)
        return {"how_many": len(response.json()["pages"]), **response.json()}


class MovieWikiClient(WikiClient):
    """This is a wiki client with movie-specific functionalities.

    Optimized for access to movie-related resources through the wikimedia api.
    """

    def _validate_wiki_response(self, search_query: str, response: dict) -> None:
        if not "pages" in response:
            raise WikiSearchPageError(
                search_query, cause=f"No pages found in response {response}"
            )

    def _validate_movies(self, search_query: str, movies: list) -> None:
        if not movies:
            raise WikiSearchPageError(search_query, cause="No movies found in response")

    def _validate_page(self, page: dict) -> None:
        if not page:
            raise PageError(page, "No page found")
        if not "key" in page:
            raise PageError(page, "No key attribute found in page")
        if page["key"] is None:
            raise PageError(page, "Page key is None")

    def _is_movie(self, page: dict) -> bool:
        self._validate_page(page)
        page_props = ["key", "description"]
        def _inner_is_movie(flag, page=page, props=page_props):
            return any(re.search(flag, page[prop]) for prop in props if page[prop] is not None)

        return any(_inner_is_movie(flag) for flag in MOVIE_RE_FLAGS)

    def search_movie(self, search_query: str, nb_results: int = 1) -> dict:
        try:
            # write_to_wiki_client_logs(message=f"Searching for {search_query}") # TODO DEBUG
            results = super().search_page(search_query, nb_results)  # requests.Response
            with open(LOGS_PATH, mode="a") as f:
                f.write("Time: " + str(datetime.datetime.now()) + "\n")
                f.write(f"Searching for {search_query}\n")
            self._validate_wiki_response(search_query, results)
            movies = [page for page in results["pages"] if self._is_movie(page)]
            self._validate_movies(search_query, movies)
            for movie in movies:
                movie["url"] = self._return_url(movie)
            return {
                "movies": movies,
                "how_many": len(movies),  # for use by external clients
            }
        except Exception as e:
            # Log the error to logfile
            handle_error(ERROR_LOGS_PATH, e)
            return {"movies": None, "how_many": 0, "error": str(e)}
