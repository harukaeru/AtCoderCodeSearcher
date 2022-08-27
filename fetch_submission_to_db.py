import sys
from scrapy.crawler import CrawlerProcess
from submission_spider import SubmissionSpider
from sql_utils import run_sqls
from schemas import Submission

def initialize():
  run_sqls([Submission.drop_table()])
  run_sqls(Submission.create_table())

def register_submissions_to_db(target_task):
  process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {
      'submission_pipeline.SubmissionPipeline': 50
    },
  })

  process.crawl(SubmissionSpider, target_task=target_task)
  process.start()

# initialize()
problem = sys.argv[1]
print(problem)
# 例: abc134_c
register_submissions_to_db(problem)