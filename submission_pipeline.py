from sql_utils import run_sqls
from schemas import AtcoderUser, Submission

class SubmissionPipeline:
  def __init__(self):
    self.strong_user_names = set([user.name for user in AtcoderUser.all()])
    # self.strong_user_names = set(['nohakai'])

  async def process_item(self, field, spider):
    atcoder_user_name = field['user_name']
    if atcoder_user_name not in self.strong_user_names:
      return

    submission = Submission(
      task_id=field['task_id'],
      atcoder_user_name=field['user_name'],
      code_size=field['code_size'],
      execution_time=field['execution_time'],
      memory=field['memory'],
      link=field['link'],
    )
    submission.create()

    return submission