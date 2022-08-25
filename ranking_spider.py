import scrapy
from schemas import AtcoderUser
from utils import get_text

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

            print([rank, user, birth_year, rating])
            # print(dir(user))
            yield {'title': user_row.css('::text').get()}

        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)