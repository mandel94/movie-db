import scrapy
from crawling_movies.loaders import MovieLoader
from crawling_movies.items import MovieItem
from datetime import datetime
import uuid


class MovieSpider(scrapy.Spider):
    name = "movie_spider"

    custom_settings = {
        "ITEM_PIPELINES": {
            "crawling_movies.pipelines.RabbitMQPipeline": 300,
        },
    }

    def __init__(self, item=None, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        self.item = item
        self.urls = {"wiki": item.get("wiki_href"), "jw": item.get("jw_href")}

    def start_requests(self):
        # Create a new MovieLoader and pass it through the meta attribute
        movie_loader = MovieLoader(item=MovieItem(), response=None)

        movie_loader.add_value("movie_id", self.generate_uuid())

        still_to_process = len(self.urls)
        for from_source, url in self.urls.items():
            still_to_process -= 1
            yield scrapy.Request(
                url=url,
                callback=self._parse(from_source),
                meta={
                    "movie_loader": movie_loader,
                    "still_to_process": still_to_process,
                },
            )

    def _parse(self, source):
        if source == "wiki":
            return self.parse_wiki
        elif source == "jw":
            return self.parse_jw
        else:
            return lambda response: None

    def parse_wiki(self, response):
        movie_loader = response.meta["movie_loader"]
        movie_loader.add_value("title", self.extract_title(response))
        movie_loader.add_value("original_title", self.extract_original_title(response))
        movie_loader.add_value("tagline", self.extract_tagline(response))
        movie_loader.add_value("plot", self.extract_plot(response))
        movie_loader.add_value("language", self.extract_language(response))
        movie_loader.add_value("country", self.extract_country(response))
        movie_loader.add_value("release_date", self.extract_release_date(response))
        movie_loader.add_value("runtime", self.extract_runtime(response))
        movie_loader.add_value("budget", self.extract_budget(response))
        movie_loader.add_value("box_office", self.extract_box_office(response))
        movie_loader.add_value("rating", self.extract_rating(response))
        movie_loader.add_value("rating_count", self.extract_rating_count(response))
        movie_loader.add_value("director_id", self.extract_director_id(response))
        movie_loader.add_value("writer_id", self.extract_writer_id(response))
        movie_loader.add_value("studio_id", self.extract_studio_id(response))
        movie_loader.add_value("distributor_id", self.extract_distributor_id(response))
        movie_loader.add_value("poster_url", self.extract_poster_url(response))
        movie_loader.add_value("trailer_url", self.extract_trailer_url(response))
        movie_loader.add_value("age_rating", self.extract_age_rating(response))
        movie_loader.add_value("imdb_id", self.extract_imdb_id(response))
        movie_loader.add_value("tmdb_id", self.extract_tmdb_id(response))
        movie_loader.add_value("homepage", self.extract_homepage(response))
        movie_loader.add_value("updated_at", self.get_timestamp())
        self._check_if_all_sources_processed(
            response.meta["still_to_process"], response
        )

    def parse_jw(self, response):
        movie_loader = response.meta["movie_loader"]
        # Extract data specific to the JW source
        # For example, if JW provides additional info, update the movie_loader here
        # movie_loader.add_value('additional_info', self.extract_additional_info(response))
        self._check_if_all_sources_processed(
            response.meta["still_to_process"], response
        )

    def _check_if_all_sources_processed(self, still_to_process, response):
        if still_to_process == 0:
            yield response.meta["movie_loader"].load_item()

    def generate_uuid(self):
        return str(uuid.uuid4())

    def get_timestamp(self):
        return datetime.now().isoformat()

    # Define each extraction function with mock values
    def extract_title(self, response):
        return "Avatar"

    def extract_original_title(self, response):
        return "Avatar"  # Same as title for now

    def extract_tagline(self, response):
        return "An epic journey awaits"

    def extract_plot(self, response):
        return "In the year 2154, a paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home."

    def extract_language(self, response):
        return "English"

    def extract_country(self, response):
        return "United States"

    def extract_release_date(self, response):
        return "2009-12-18"

    def extract_runtime(self, response):
        return "162 minutes"

    def extract_budget(self, response):
        return "$237 million"

    def extract_box_office(self, response):
        return "$2.847 billion"

    def extract_rating(self, response):
        return "7.8"

    def extract_rating_count(self, response):
        return "876,543"

    def extract_director_id(self, response):
        return "James Cameron"

    def extract_writer_id(self, response):
        return "James Cameron"

    def extract_studio_id(self, response):
        return "20th Century Fox"

    def extract_distributor_id(self, response):
        return "20th Century Fox"

    def extract_poster_url(self, response):
        return "https://example.com/poster.jpg"

    def extract_trailer_url(self, response):
        return "https://example.com/trailer.mp4"

    def extract_age_rating(self, response):
        return "PG-13"

    def extract_imdb_id(self, response):
        return "tt0499549"

    def extract_tmdb_id(self, response):
        return "19995"

    def extract_homepage(self, response):
        return "https://www.avatarmovie.com/"
