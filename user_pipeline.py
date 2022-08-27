from sql_utils import run_sqls

class UserPipeline:
  async def process_item(self, ranking_field, spider):
    atcoder_user = ranking_field['user']
    run_sqls([atcoder_user.create()])

    return atcoder_user