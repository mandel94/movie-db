import scrapy
from crawling_movies.loaders import MovieLoader
from crawling_movies.items import MovieItem
from datetime import datetime
import uuid
import logging


class MovieSpider(scrapy.Spider):
    name = "scrape_movie"

    custom_settings = {
        "ITEM_PIPELINES": {
            "crawling_movies.pipelines.RabbitMQPipeline": 300,
        },
        "LOG_LEVEL": "ERROR",
    }

    def __init__(
        self,
        item_info=None,
        rabbitmq_connection=None,
        rabbitmq_queue=None,
        *args,
        **kwargs
    ):
        super(MovieSpider, self).__init__(*args, **kwargs)
        self.item_info = item_info
        self.rabbitmq_connection = rabbitmq_connection
        self.rabbitmq_queue = rabbitmq_queue
        self.urls = {
            "wiki": self.item_info.get("wiki_href"),
            "jw": self.item_info.get("jw_href"),
        }

    def start_requests(self):
        # This method must return an iterable with the first Requests to crawl for this spider.
        # It is called by Scrapy when the spider is opened for scraping. Scrapy calls it only once, so it is safe to implement start_requests() as a generator.
        # Create a new MovieLoader and pass it through the meta attribute
        movie_loader = MovieLoader(item=MovieItem(), response=None)
        movie_loader.add_value("movie_id", self.generate_uuid())

        initial_url = self.urls.get("wiki")  # Start scraping from wiki
        yield scrapy.Request(
            url=initial_url,
            callback=self.parse_wiki,
            meta={"movie_loader": movie_loader, "from_source": "wiki"},
        )

    def parse_wiki(self, response):
        # Parse the initial page and extract the title
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
        movie_loader.add_value("updated_at", self.get_timestamp())
        yield scrapy.Request(
            url=self.urls.get("jw"),
            callback=self.parse_jw,
            meta={"movie_loader": movie_loader},
        )

    def parse_jw(self, response):
        movie_loader = response.meta["movie_loader"]
        # Extract data specific to the JW source
        # For example, if JW provides additional info, update the movie_loader here
        # movie_loader.add_value('additional_info', self.extract_additional_info(response))
        movie_loader.add_value("homepage", self.extract_homepage(response))
        # Get back to parse_wiki to extract the next source
        # yield scrapy.Request(
        #     url=self.urls.get("imdb"),
        #     callback=self.parse_imdb,
        #     meta={"movie_loader": movie_loader}
        # )
        return movie_loader.load_item()

    def parse_imdb(self, response):
        movie_loader = response.meta["movie_loader"]
        # Extract data specific to the IMDB source
        # For example, if IMDB provides additional info, update the movie_loader here
        # movie_loader.add_value('additional_info', self.extract_additional_info(response))
        # Save the item
        return movie_loader.load_item()

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
