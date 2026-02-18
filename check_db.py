import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM schedule")
print(cursor.fetchall())

conn.close()
