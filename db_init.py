import sqlite3

db = sqlite3.connect('database.sqlite')
c = db.cursor()

try:
    c.executescript(open('schema.sql').read())
    db.commit()
    print("Successfully initialized database.")
except sqlite3.DatabaseError as er:
    print("Database initialization has failed.")
    print(er)

db.close()
