import sqlite3

conn = sqlite3.connect('database.sqlite')

cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         email TEXT UNIQUE NOT NULL
#     )
# ''')


# cursor.execute('''
#     INSERT INTO users (name, email)
#     VALUES (?, ?)
# ''', ('John Doe', 'john@example.com'))


# conn.commit()


cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
