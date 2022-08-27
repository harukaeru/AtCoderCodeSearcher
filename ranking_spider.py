import scrapy
from schemas import AtcoderUser
from parser_utils import get_text

class RankingSpider(scrapy.Spider):
    name = 'rankingspider'
    # start_urls = ['https://atcoder.jp/ranking?contestType=algo&page=1']
    start_urls = ['http://localhost:8000/ranking_atcoder.html']

    def parse(self, response):
        for user_row in response.css('table.table-bordered tbody tr'):
            rank = get_text(user_row.css('td:nth-child(1)').get())
            birth_year = get_text(user_row.css('td:nth-child(3)').get())
            rating = get_text(user_row.css('td:nth-child(4) b').get())

            user_css = user_row.css('td:nth-child(2)')
            country_code = user_css.css('a:nth-child(1)').attrib['href'].split('Country=')[-1]
            name = get_text(user_css.css('a.username span').get())
            affiliation = get_text(user_css.css('span.ranking-affiliation').get())

            user = AtcoderUser(
                country_code=country_code,
                name=name,
                affiliation=affiliation,
                rank=rank,
                birth_year=birth_year,
                rating=rating,
            )

            yield { 'user': user }

        next_page = response.css('ul.pagination li.active + li a::attr(href)').get()
        print('next_page', next_page)
        if next_page is not None:
            yield response.follow(next_page, self.parse)