from itertools import groupby
from app import get_db_connection

conn = get_db_connection()
todos = conn.execute('SELECT i.id, i.done, i.content, l.title \
                      FROM items i JOIN lists l \
                      ON i.list_id = l.id ORDER BY l.title;').fetchall()

lists = {}

for k, g in groupby(todos, key=lambda t: t['title']):
    lists[k] = list(g)

for list_, items in lists.items():
    print(list_)
    for item in items:
        print('    ', item['content'], '| id:',
              item['id'], '| done:', item['done'])
