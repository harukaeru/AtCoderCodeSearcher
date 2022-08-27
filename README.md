# AtCoderCodeSearcher

Scrapyを使って、AtCoderのランキングに載っている上位のユーザーと、各問題でのユーザーの提出結果をクロールしてsqlite3に格納します。

格納されたデータはsqliteに保存されているので、以下のように好きに結合してデータを得ることができます。これはSQLPadというクライアントを使って接続している図です。

<img width="1727" alt="image" src="https://user-images.githubusercontent.com/5797788/187029453-b78a8161-f8b1-47f3-84bc-b9977df992bc.png">

他人向けに作っていないので、使いにくいと思います。気が向いたらええ感じにサービスにします。

## 使い方

```python
# ランキング情報をsqlite3に入れます（上位5100位まで）
$ python3 python3 fetch_ranking_to_db.py

# 提出情報を格納します。ランキング情報に載っているユーザーしかデータベースには登録しません
# 初期化とかは適当なので、適当にソースを読んでいい感じにしてください
$ python3 fetch_submission_to_db.py abc134_c

$ sqlite3 atcoder.db
sqlite> select * from atcoder_user LIMIT 1;
BY|tourist|ITMO University|1|1994|3976
```

## Philosophy

最初、スクレイピングするだけにとどめようとしたので、あとからsqliteを使うことにして、そのせいでなんかORMapperもどきを自作しています。

↓こういうの

```python
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
```

## Ref

Scrapyの使い方はここがわかりやすいです。

- https://docs.scrapy.org/en/latest/intro/tutorial.html
- https://docs.scrapy.org/en/latest/topics/architecture.html
