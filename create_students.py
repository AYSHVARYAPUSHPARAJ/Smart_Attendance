import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    class_name TEXT
)
""")

# Insert sample students
students = [
    ("Arjun", "CSE_3rdYear"),
    ("Priya", "CSE_3rdYear"),
    ("Rahul", "CSE_3rdYear"),
    ("Anjali", "CSE_3rdYear"),
    ("Kiran", "CSE_3rdYear"),
    ("Vikram", "CSE_3rdYear"),
    ("Sneha", "CSE_3rdYear"),
    ("Rohit", "CSE_3rdYear"),
    ("Divya", "CSE_3rdYear"),
    ("Manoj", "CSE_3rdYear"),
    ("Aojun", "CSE_3rdYear"),
    ("Poiya", "CSE_3rdYear"),
    ("Raohul", "CSE_3rdYear"),
    ("Anjoali", "CSE_3rdYear"),
    ("Kiraon", "CSE_3rdYear"),
    ("Vikraom", "CSE_3rdYear"),
    ("Snehao", "CSE_3rdYear"),
    ("Rohito", "CSE_3rdYear"),
    ("Divyao", "CSE_3rdYear"),
    ("Manojo", "CSE_3rdYear")
]

cursor.executemany(
    "INSERT INTO students (name, class_name) VALUES (?, ?)",
    students
)

conn.commit()
conn.close()

print("Students table created and records inserted.")
