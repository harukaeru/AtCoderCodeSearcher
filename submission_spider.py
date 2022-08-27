import scrapy
from parser_utils import get_text

class SubmissionSpider(scrapy.Spider):
    name = 'submission_spider'
    TEMPLATE_START_URL = 'https://atcoder.jp/contests/{contest_id}/submissions?f.Task={target_task}&f.LanguageName=Python3&f.Status=AC&f.User='
    # TEMPLATE_START_URL = 'http://localhost:8000/submission.html?f.Task={target_task}'

    # target_task='abc123_c'
    def start_requests(self):
        contest_id = self.target_task.split('_')[0]
        start_url = self.TEMPLATE_START_URL.format(target_task=self.target_task, contest_id=contest_id)
        yield scrapy.Request(start_url)

    def parse(self, response):
        for answer_row in response.css('table.table-bordered tbody tr'):
            user_name = get_text(answer_row.css('td:nth-child(3) a').get())
            size = get_text(answer_row.css('td:nth-child(6)').get()).replace(' Byte', '')
            execution_time = get_text(answer_row.css('td:nth-child(8)').get()).replace(' ms', '')
            memory = get_text(answer_row.css('td:nth-child(9)').get()).replace(' KB', '')
            link = answer_row.css('td:nth-child(10) a::attr(href)').get()

            yield {
                'task_id': self.target_task,
                'user_name': user_name,
                'code_size': size,
                'execution_time': execution_time,
                'memory': memory,
                'link': link,
            }

        next_page = response.css('ul.pagination li.active + li a::attr(href)').get()
        print('next_page', next_page)
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        # for title in response.css('.oxy-post-title'):
        #     yield {'title': title.css('::text').get()}

        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)