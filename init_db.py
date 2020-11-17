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

cur.execute("INSERT INTO assignees (name) VALUES (?)", ('Bob',))
cur.execute("INSERT INTO assignees (name) VALUES (?)", ('Jane',))
cur.execute("INSERT INTO assignees (name) VALUES (?)", ('Alice',))
cur.execute("INSERT INTO assignees (name) VALUES (?)", ('Mike',))

# Assign "Morning meeting" to "Bob"
cur.execute("INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)",
            (1, 1))

# Assign "Morning meeting" to "Jane"
cur.execute("INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)",
            (1, 2))

# Assign "Morning meeting" to "Mike"
cur.execute("INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)",
            (1, 4))

# Assign "Buy fruit" to "Bob"
cur.execute("INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)",
            (2, 1))

connection.commit()
connection.close()
