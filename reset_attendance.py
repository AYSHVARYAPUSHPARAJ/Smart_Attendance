import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Delete old attendance table
cursor.execute("DROP TABLE IF EXISTS attendance")

# Create new attendance table
cursor.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    class_name TEXT,
    student_id INTEGER,
    date TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Attendance table reset successfully.")
