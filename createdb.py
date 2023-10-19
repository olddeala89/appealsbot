import datetime
import sqlite3

conn = sqlite3.connect('requests.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE appeals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auditorium VARCHAR(10),
    problem VARCHAR(30),
    user_name VARCHAR(30),
    request_time DATETIME
);""")

conn.commit()

conn.close()

conn = None
cursor = None
del conn
del cursor