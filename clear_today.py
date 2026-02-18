import sqlite3
from datetime import datetime

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

today = datetime.now().strftime("%Y-%m-%d")

cursor.execute("DELETE FROM attendance WHERE date=?", (today,))
conn.commit()
conn.close()

print("Today's attendance cleared.")
