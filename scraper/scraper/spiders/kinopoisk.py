import re
from urllib.parse import unquote

import scrapy
from scrapy.loader import ItemLoader

from scraper.items import FilmItem, LetterboxdItem

from datetime import datetime

#to disable errors with pyinstaller
import scrapy.utils.misc
import scrapy.core.scraper

def warn_on_generator_with_return_value_stub(spider, callable):
    pass

scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub


class KinopoiskLoader(ItemLoader):
    pass

class LetterboxdLoader(ItemLoader):
    pass

class KinopoiskSpider(scrapy.Spider):
    name = 'kinopoisk'
    allowed_domains = ['www.kinopoisk.ru']
    ITEMS_PER_PAGE = 200
    BASE_URL = 'https://www.kinopoisk.ru/user/{user_id}/votes/list/ord/date/perpage/{items_per_page}/#list'
    PAGES = 'https://www.kinopoisk.ru/user/{user_id}/votes/list/ord/date/page/{page_no}/#list'
    COOKIES = {
        'location': '1',
        'ya_sess_id': ''
    }

    custom_settings = {
        'FEEDS': {
            'ratings.csv' : {
                'format': 'csv'
            }
        }
    }

    def get_score(self, encoded):
        result = re.findall('\'(\d+)', unquote(encoded))
        return result[0]

    def start_requests(self):
        self.COOKIES['ya_sess_id'] = self.ya_sess_id
        url = self.BASE_URL.format(user_id=self.user_id, items_per_page=self.ITEMS_PER_PAGE)
        yield scrapy.Request(url=url, callback=self.parse_list, cookies=self.COOKIES)

    def parse_list(self, response):
        count = int(response.css('table.fontsize10 tr:first-child td')[2].root.text)
        for page in range(1, count // self.ITEMS_PER_PAGE + 2):
            url = self.PAGES.format(user_id=self.user_id, page_no=page)
            yield scrapy.Request(url=url, callback=self.parse_page, cookies=self.COOKIES)

    def parse_page(self, response):
        if self.letterboxd == 1:
            for _, item in enumerate(response.css('div.profileFilmsList .item')):
                loader = LetterboxdLoader(item=LetterboxdItem(), response=response, selector=item)
                score = item.xpath('script/text()')[0].root
                loader.add_value('Rating10', self.get_score(score.split(';')[0][35:-4].split("`),`")[0]))
                date_str = item.xpath('div[@class="date"]/text()')[0].root
                date = datetime.strptime(date_str, '%d.%m.%Y, %H:%M')
                date_time_str = date.strftime("%Y-%m-%d")
                loader.add_xpath('Title', 'div/div[@class="nameEng"]/text()')
                loader.add_value('WatchedDate', date_time_str)
                loader.add_xpath('Rating10', 'div[@class="selects vote_widget"]/span/div/text()')
                yield loader.load_item()
        
        else:
            for _, item in enumerate(response.css('div.profileFilmsList .item')):
                loader = KinopoiskLoader(item=FilmItem(), response=response, selector=item)
                link = item.xpath('div/div[@class="nameRus"]/a')[0].attrib['href']
                score = item.xpath('script/text()')[0].root
                loader.add_value('score', self.get_score(score.split(';')[0][35:-4].split("`),`")[0]))
                loader.add_value('link', f'https://{self.allowed_domains[0]}{link}')
                try:
                    description = re.match('^(.*)\s\((\d{4})\)$', item.xpath('div/div[@class="nameRus"]/a/text()')[0].root)
                    loader.add_value('title_ru', description.group(1))
                    loader.add_value('year', description.group(2))
                except:
                    loader.add_xpath('title_ru', 'div/div[@class="nameRus"]/a/text()')
                loader.add_xpath('no', 'div[@class="num"]/text()')
                loader.add_xpath('title_en', 'div/div[@class="nameEng"]/text()')
                loader.add_xpath('date', 'div[@class="date"]/text()')

                loader.add_xpath('score', 'div[@class="selects vote_widget"]/span/div/text()')
                yield loader.load_item()
