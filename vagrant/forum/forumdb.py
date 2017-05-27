# "Database code" for the DB Forum.

import datetime
import psycopg2 as db

POSTS = [("This is the first post.", datetime.datetime.now())]
DBNAME = 'forum'

def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = db.connect(database=DBNAME)
  c = conn.cursor()
  c.execute('select content, time, rom posts order by time desc')
  l = c.fetchall()
  conn.close()
  return l

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  conn = db.connect(database=DBNAME)
  c = conn.cursor()
  c.execute('insert into posts values (%s)', (content,))
  conn.commit()
  conn.close()
