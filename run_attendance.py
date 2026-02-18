from recognize import recognize_teacher
from dashboard import open_dashboard

print("Starting Smart Attendance...")

teacher_id = recognize_teacher()

if teacher_id:
    print(f"Recognized Teacher ID: {teacher_id}")
    open_dashboard(teacher_id)
else:
    print("Access Denied: Teacher not recognized.")

