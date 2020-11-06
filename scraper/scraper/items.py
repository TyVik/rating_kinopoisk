# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class FilmItem(scrapy.Item):
    no = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    title_ru = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    title_en = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    year = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    link = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    date = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    score = scrapy.Field(input_processor=TakeFirst(), output_processor=TakeFirst())
