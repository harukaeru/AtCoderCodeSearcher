import importlib
from sql_utils import create_sql_statement, run_sqls

def instantiate(class_name):
  def deco(func):
    def actual_func(*args, **kwargs):
      Model = getattr(importlib.import_module('schemas'), class_name)
      sqls = func(*args, **kwargs)

      objects = []
      # breakpoint()
      rows = run_sqls(sqls)
      for row in rows:
        objects.append(Model(*row))
      return objects
    return actual_func
  return deco

class AtcoderUser:
  @classmethod
  def create_table(cls):
    return '''
      CREATE TABLE atcoder_user (
        country_code, name, affiliation, rank INT, birth_year INT, rating INT,
        CONSTRAINT name_should_be_unique UNIQUE (name)
      )
    '''
  
  @classmethod
  def drop_table(cls):
    return 'DROP TABLE atcoder_user'

  def __init__(self, country_code, name, affiliation, rank, birth_year, rating):
    self.country_code = country_code
    self.name = name
    self.affiliation = affiliation
    self.rank = rank
    self.birth_year = birth_year
    self.rating = rating

  def __repr__(self):
    return f'<レート: {self.rating}, ユーザ名: {self.name}, 国: {self.country_code}>'

  def create(self):
    return create_sql_statement(
      "INSERT INTO atcoder_user VALUES ({}, {}, {}, {}, {}, {})",
      self.country_code, self.name, self.affiliation, self.rank, self.birth_year, self.rating
    )

  @instantiate('AtcoderUser')
  def all():
    return f"SELECT * FROM atcoder_user"

  @instantiate('AtcoderUser')
  def where(where_clause):
    return f"SELECT * FROM atcoder_user WHERE {where_clause}"

class Submission:
  @classmethod
  def create_table(cls):
    return [
      '''
        CREATE TABLE submission (
          task_id, atcoder_user_name, code_size INT, execution_time INT, memory INT, link,
          FOREIGN KEY (atcoder_user_name) REFERENCES atcoder_user(name)
        )
      ''',
      'CREATE INDEX task_id_index ON submission(task_id)'
    ]
  
  @classmethod
  def drop_table(cls):
    return 'DROP TABLE submission'

  def __init__(self, task_id, atcoder_user_name, code_size, execution_time, memory, link):
    self.task_id = task_id
    self.atcoder_user_name = atcoder_user_name
    self.code_size = code_size
    self.execution_time = execution_time
    self.memory = memory
    self.link = link

  def __repr__(self):
    return f'<TaskID: {self.task_id}, ユーザ名: {self.atcoder_user_name}, Size: {self.code_size}KB, 実行時間: {self.execution_time}ms>'

  @instantiate('Submission')
  def create(self):
    return create_sql_statement(
      "INSERT INTO submission VALUES ({}, {}, {}, {}, {}, {})",
      self.task_id, self.atcoder_user_name, self.code_size, self.execution_time, self.memory, self.link
    )

  @classmethod
  def delete(cls, task_id):
    return run_sqls(f'DELETE FROM submission WHERE task_id = "{task_id}"')