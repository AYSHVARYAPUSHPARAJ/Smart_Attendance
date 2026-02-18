import sqlite3
import os
print(os.getcwd())


conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM attendance")
print(cursor.fetchall())

conn.close()
