# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieList(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Define the fields for your item here like:
    movie_list_id = scrapy.Field()
    title = scrapy.Field()
    jw_href = scrapy.Field() # JustWatch href
    wiki_href = scrapy.Field() # Wikipedia href


class MovieItem(scrapy.Item):
    # Define the fields for your item here like:
    movie_id = scrapy.Field()  # Required field
    title = scrapy.Field(default=None)
    original_title = scrapy.Field(default=None)
    tagline = scrapy.Field(default=None)
    plot = scrapy.Field(default=None)
    language = scrapy.Field(default=None)
    country = scrapy.Field(default=None)
    release_date = scrapy.Field(default=None)
    runtime = scrapy.Field(default=None)
    budget = scrapy.Field(default=None)
    box_office = scrapy.Field(default=None)
    rating = scrapy.Field(default=None)
    rating_count = scrapy.Field(default=None)
    director_id = scrapy.Field(default=None)
    writer_id = scrapy.Field(default=None)
    studio_id = scrapy.Field(default=None)
    distributor_id = scrapy.Field(default=None)
    poster_url = scrapy.Field(default=None)
    trailer_url = scrapy.Field(default=None)
    age_rating = scrapy.Field(default=None)
    imdb_id = scrapy.Field(default=None)
    tmdb_id = scrapy.Field(default=None)
    homepage = scrapy.Field(default=None)
    created_at = scrapy.Field(default=None)
    updated_at = scrapy.Field(default=None)
