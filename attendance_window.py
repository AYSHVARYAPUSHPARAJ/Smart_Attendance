import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ---------------- ATTENDANCE WINDOW ----------------
def open_attendance_window(teacher_id, class_name=None):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    # If class_name is not provided, get current active class
    if not class_name:
        current_day = datetime.now().strftime("%A")
        current_time = datetime.now().strftime("%H:%M")
        cursor.execute("""
            SELECT class_name FROM schedule
            WHERE teacher_id=? AND day=? AND start_time<=? AND end_time>=?
        """, (teacher_id, current_day, current_time, current_time))
        res = cursor.fetchone()
        if res:
            class_name = res[0]
        else:
            messagebox.showwarning("Warning", "No active class right now!")
            conn.close()
            return

    # Check if attendance already marked
    cursor.execute("""
        SELECT * FROM attendance
        WHERE class_name=? AND date=?
    """, (class_name, today))
    if cursor.fetchone():
        messagebox.showwarning("Warning", f"Attendance already marked for {class_name} today!")
        conn.close()
        return

    # Fetch students for this class
    cursor.execute("SELECT id, name FROM students WHERE class_name=?", (class_name,))
    students = cursor.fetchall()

    if not students:
        messagebox.showwarning("Warning", f"No students found for class {class_name}!")
        conn.close()
        return

    conn.close()

    # ---------------- UI START ----------------
    root = tk.Tk()
    root.title("Smart Attendance System")
    root.geometry("520x650")
    root.configure(bg="#f4f6f8")

    title = tk.Label(root, text="Smart Attendance",
                     font=("Segoe UI", 20, "bold"),
                     bg="#f4f6f8")
    title.pack(pady=15)

    info_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    info_frame.pack(pady=10, padx=25, fill="x")

    tk.Label(info_frame, text=f"Class: {class_name}",
             font=("Segoe UI", 12),
             bg="#ffffff").pack(pady=5)

    tk.Label(info_frame, text=f"Date: {today}",
             font=("Segoe UI", 12),
             bg="#ffffff").pack(pady=5)

    student_vars = {}

    student_frame = tk.Frame(root, bg="#f4f6f8")
    student_frame.pack(pady=10)

    for student_id, name in students:
        var = tk.IntVar(value=1)  # default all present
        chk = tk.Checkbutton(student_frame,
                             text=name,
                             variable=var,
                             font=("Segoe UI", 11),
                             bg="#f4f6f8")
        chk.pack(anchor="w", padx=25, pady=2)
        student_vars[student_id] = var

    # ---------------- FUNCTIONS ----------------
    def mark_all_present():
        for var in student_vars.values():
            var.set(1)

    def mark_all_absent():
        for var in student_vars.values():
            var.set(0)

    def save_attendance():
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        for student_id, var in student_vars.items():
            status = "Present" if var.get() == 1 else "Absent"
            cursor.execute("""
                INSERT INTO attendance
                (teacher_id, class_name, student_id, date, status)
                VALUES (?, ?, ?, ?, ?)
            """, (teacher_id, class_name, student_id, today, status))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Attendance Saved Successfully!")
        root.destroy()

    # ---------------- BUTTONS ----------------
    button_frame = tk.Frame(root, bg="#f4f6f8")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Mark All Present",
              font=("Segoe UI", 10),
              bg="#4CAF50", fg="white",
              width=16,
              command=mark_all_present).grid(row=0, column=0, padx=12)

    tk.Button(button_frame, text="Mark All Absent",
              font=("Segoe UI", 10),
              bg="#f44336", fg="white",
              width=16,
              command=mark_all_absent).grid(row=0, column=1, padx=12)

    tk.Button(root, text="Save Attendance",
              font=("Segoe UI", 13, "bold"),
              bg="#2196F3", fg="white",
              width=22,
              command=save_attendance).pack(pady=25)

    root.mainloop()


