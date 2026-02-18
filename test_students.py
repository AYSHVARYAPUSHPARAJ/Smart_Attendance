import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

class_name = "CSE_3rdYear"

cursor.execute("SELECT id, name FROM students WHERE class_name=?", (class_name,))
students = cursor.fetchall()

print("Students in class:", students)

conn.close()
