# Smart Attendance System

A Python-based **Smart Attendance System** using **face recognition**.  
Automatically marks teacher attendance based on their face and class schedule.

---

## **Features**

- Teacher login via **face recognition**.
- Displays **active class** based on schedule.
- Attendance marking window with **present/absent checkboxes**.
- Saves attendance to a database (`attendance.db`) and can generate reports.
- GUI made with **Tkinter**.

---

## **Setup Instructions**

1. **Clone the repository:**
git clone https://github.com/your-username/smart-attendance.git
cd smart-attendance

2. **Install Python dependencies:**
pip install opencv-python numpy tk

3.**Create the database:**
python database.py
python create_students.py

4.**Train the face recognition model:**
python train_model.py

5.**Run the system:**
python run_attendance.py
