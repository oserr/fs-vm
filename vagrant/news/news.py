#!/usr/bin/env python3
# news.py

import psycopg2 as db

DBNAME = 'news'

QUERY_MOST_POPULAR_ARTICLE="""
select title, count(*) as total_views
from articles, log
where articles.slug = right(path, -9)
group by articles.title
order by total_views desc
limit 3;
"""

QUERY_MOST_POPULAR_AUTHOR="""
select authors.name, count(*) as total_views
from authors, articles, log
where authors.id = articles.author and articles.slug = right(path, -9)
group by authors.name
order by total_views desc
limit 3;
"""

QUERY_ERR_RATE_PER_DAY="""
select hits_per_day.log_day, 100.0*err_per_day.total/hits_per_day.total as err_percent
from
  (select time::date as log_day, count(*) as total
   from log where status = '200 OK'
   group by log_day) as hits_per_day,
  (select time::date as log_day, count(*) as total
   from log where status != '200 OK'
   group by log_day) as err_per_day
where hits_per_day.log_day = err_per_day.log_day
  and 1.0*err_per_day.total/hits_per_day.total >= 0.01;
"""

if __name__ == '__main__':
    conn = db.connect(database=DBNAME)
    c = conn.cursor()

    c.execute(QUERY_MOST_POPULAR_ARTICLE)
    table = c.fetchall()
    print('The 3 most popular articles by total views')
    print('(title, total views)')
    print('------------------------------------------')
    for row in table:
        print(row)
    print()

    c.execute(QUERY_MOST_POPULAR_AUTHOR)
    table = c.fetchall()
    print('The 3 most popular authors by total views')
    print('(author, total views)')
    print('-----------------------------------------')
    for row in table:
        print(row)
    print()

    c.execute(QUERY_ERR_RATE_PER_DAY)
    table = c.fetchall()
    print('Dates with bad request rate higher than 1%')
    print('(date, percent of bad requests)')
    print('------------------------------------------')
    for row in table:
        # Explicit %s to force string formatting
        print('(%s, %s)' % row)
