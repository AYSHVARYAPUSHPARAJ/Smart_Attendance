import tkinter as tk
import sqlite3
from datetime import datetime
from attendance_window import open_attendance_window

def open_dashboard(teacher_id):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, department, subject FROM teachers WHERE id=?", (teacher_id,))
    teacher = cursor.fetchone()

    if not teacher:
        print("Teacher not found")
        return

    name, dept, subject = teacher
    today_day = datetime.now().strftime("%A")
    current_time = datetime.now().strftime("%H:%M")

    # Get today's schedule
    cursor.execute("""
        SELECT start_time, end_time, class_name
        FROM schedule
        WHERE teacher_id=? AND day=?
    """, (teacher_id, today_day))
    schedules = cursor.fetchall()

    # Find active class
    active_class = None
    for start, end, class_name in schedules:
        if start <= current_time <= end:
            active_class = class_name
            break

    root = tk.Tk()
    root.title("Teacher Dashboard")
    root.geometry("600x500")
    root.configure(bg="#eef2f7")

    tk.Label(root, text="Teacher Dashboard",
             font=("Segoe UI", 20, "bold"),
             bg="#eef2f7").pack(pady=15)

    info_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
    info_frame.pack(pady=10, padx=30, fill="x")

    tk.Label(info_frame, text=f"Name: {name}", font=("Segoe UI", 12), bg="white").pack(pady=5)
    tk.Label(info_frame, text=f"Department: {dept}", font=("Segoe UI", 12), bg="white").pack(pady=5)
    tk.Label(info_frame, text=f"Subject: {subject}", font=("Segoe UI", 12), bg="white").pack(pady=5)

    tk.Label(root, text="Today's Schedule", font=("Segoe UI", 14, "bold"), bg="#eef2f7").pack(pady=10)
    schedule_frame = tk.Frame(root, bg="#eef2f7")
    schedule_frame.pack()
    for start, end, class_name in schedules:
        tk.Label(schedule_frame, text=f"{start} - {end}  |  {class_name}", font=("Segoe UI", 11), bg="#eef2f7").pack(anchor="w")

    # Open attendance button automatically if active class exists
    if active_class:
        tk.Button(root,
                  text=f"Open Attendance ({active_class})",
                  font=("Segoe UI", 12, "bold"),
                  bg="#2196F3", fg="white",
                  width=25,
                  command=lambda: open_attendance_window(teacher_id, active_class)
                  ).pack(pady=20)
    else:
        tk.Label(root, text="No Active Class Now", font=("Segoe UI", 12), fg="red", bg="#eef2f7").pack(pady=15)

    root.mainloop()

