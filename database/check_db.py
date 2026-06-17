import sqlite3

conn = sqlite3.connect("railway.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT * FROM trains")

trains = cursor.fetchall()

print(trains)

conn.close()