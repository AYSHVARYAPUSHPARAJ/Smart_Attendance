import sqlite3

def create_connection():
    conn = sqlite3.connect("attendance.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        subject TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        day TEXT,
        start_time TEXT,
        end_time TEXT,
        class_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        class_name TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")


def insert_sample_teacher():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teachers WHERE name = ?", ("Dr. Meena",))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("""
        INSERT INTO teachers (name, department, subject)
        VALUES (?, ?, ?)
        """, ("Dr. Meena", "CSE", "Machine Learning"))
        conn.commit()
        print("Sample teacher inserted.")
    else:
        print("Teacher already exists.")

    conn.close()



def insert_sample_schedule():
    conn = create_connection()
    cursor = conn.cursor()

    # Delete old schedule entries for teacher 1
    cursor.execute("DELETE FROM schedule WHERE teacher_id=?", (1,))

    # Insert new schedule
    cursor.execute("""
    INSERT INTO schedule (teacher_id, day, start_time, end_time, class_name)
    VALUES (?, ?, ?, ?, ?)
    """, (1, datetime.datetime.now().strftime("%A"), "22:00", "24:00", "CSE_3rdYear"))

    conn.commit()
    conn.close()
    print("Sample schedule inserted.")

    
def get_teacher_by_id(teacher_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teachers WHERE id = ?", (teacher_id,))
    teacher = cursor.fetchone()

    conn.close()
    return teacher


def get_schedule_for_day(teacher_id, day):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM schedule 
    WHERE teacher_id = ? AND day = ?
    """, (teacher_id, day))

    schedules = cursor.fetchall()

    conn.close()
    return schedules

def check_current_class(teacher_id):
    import datetime

    current_day = datetime.datetime.now().strftime("%A")
    current_time = datetime.datetime.now().strftime("%H:%M")

    schedules = get_schedule_for_day(teacher_id, current_day)

    for schedule in schedules:
        start_time = schedule[3]
        end_time = schedule[4]
        class_name = schedule[5]

        if start_time <= current_time <= end_time:
            return class_name

    return None


import datetime

if __name__ == "__main__":
    create_tables()
    insert_sample_teacher()
    insert_sample_schedule()

    teacher = get_teacher_by_id(1)
    print("Teacher Data:", teacher)

    active_class = check_current_class(1)

    if active_class:
        print("Current Active Class:", active_class)
    else:
        print("No class scheduled right now.")


