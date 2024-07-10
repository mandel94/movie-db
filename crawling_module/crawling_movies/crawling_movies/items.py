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
