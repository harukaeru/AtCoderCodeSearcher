from scrapy.crawler import CrawlerProcess
from ranking_spider import RankingSpider
from sql_utils import run_sqls
from schemas import AtcoderUser

process = CrawlerProcess(settings={
  'ITEM_PIPELINES': {
    'user_pipeline.UserPipeline': 50
  },
  'DEPTH_LIMIT': 50,
})

run_sqls([AtcoderUser.drop_table()])
run_sqls([AtcoderUser.create_table()])
process.crawl(RankingSpider)
process.start()