from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst



class MovieListLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MovieLoader(ItemLoader):
    default_output_processor = TakeFirst()