import functools
import sqlite3

def run_sqls(sqls):
  if isinstance(sqls, str):
    sqls = [sqls]
  # breakpoint()

  con = sqlite3.connect("atcoder.db")
  cur = con.cursor()
  rows = []
  for sql in sqls:
    print('sql', sql)
    row = cur.execute(sql)
    # breakpoint()
    for result in row.fetchall():
      rows.append(result)
  con.commit()
  con.close()
  return rows

def create_sql_statement(sql_template, *values):
  repr_values = [repr(value) for value in values]
  return sql_template.format(*repr_values)