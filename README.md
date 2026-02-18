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


## ** Project Structure**

smart-attendance/
├── attendance_window.py
├── dashboard.py
├── database.py
├── create_students.py
├── train_model.py
├── recognize.py
├── run_attendance.py
├── dataset/          
└── README.md

Run the system:

python run_attendance.py
