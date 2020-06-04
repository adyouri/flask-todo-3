import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO lists (title) VALUES (?)", ('Work',))
cur.execute("INSERT INTO lists (title) VALUES (?)", ('Home',))
cur.execute("INSERT INTO lists (title) VALUES (?)", ('Study',))

cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)",
            (1, 'Morning meeting')
            )

cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)",
            (2, 'Buy fruit')
            )

cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)",
            (2, 'Cook dinner')
            )

cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)",
            (3, 'Learn Flask')
            )

cur.execute("INSERT INTO items (list_id, content) VALUES (?, ?)",
            (3, 'Learn SQLite')
            )

connection.commit()
connection.close()
