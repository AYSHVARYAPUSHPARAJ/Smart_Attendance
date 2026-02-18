import sqlite3
from datetime import datetime

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

today_day = datetime.now().strftime("%A")

cursor.execute("""
INSERT INTO schedule (teacher_id, day, start_time, end_time, class_name)
VALUES (?, ?, ?, ?, ?)
""", (1, today_day, "20:00", "22:00", "Demo_Class"))

conn.commit()
conn.close()

print("Test schedule inserted.")
