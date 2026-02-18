import cv2
import sqlite3
from datetime import datetime

def recognize_teacher():
    # ------------------ Load Recognizer & Cascade ------------------
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainer.yml")
    except Exception as e:
        print("Error loading trainer.yml:", e)
        return None

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # ------------------ Connect to DB ------------------
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    # ------------------ Open Camera ------------------
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera. Check if it's busy or connected.")
        return None

    print("Camera started. Press ESC to exit.")

    teacher_id = None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]

            # Predict ID
            try:
                id_predicted, confidence = recognizer.predict(face)
            except Exception as e:
                print("Prediction error:", e)
                continue

            if confidence < 100:  # threshold for recognizing
                cursor.execute("SELECT name FROM teachers WHERE id=?", (id_predicted,))
                result = cursor.fetchone()

                if result:
                    name = result[0]

                    # Check active class
                    today_day = datetime.now().strftime("%A")
                    current_time = datetime.now().strftime("%H:%M")

                    cursor.execute("""
                        SELECT class_name FROM schedule
                        WHERE teacher_id=? AND day=? AND start_time <= ? AND end_time >= ?
                    """, (id_predicted, today_day, current_time, current_time))

                    class_result = cursor.fetchone()

                    if class_result:
                        class_name = class_result[0]
                        text = f"{name} - {class_name}"
                    else:
                        text = f"{name} - No Class Now"

                    teacher_id = id_predicted
                else:
                    text = "Unknown"
            else:
                text = "Unknown"

            # Draw rectangle and name
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Smart Attendance - Recognition", frame)

        # ESC to exit
        key = cv2.waitKey(1)
        if key == 27 or teacher_id is not None:  # ESC or recognized
            break

    cam.release()
    cv2.destroyAllWindows()
    conn.close()

    if teacher_id:
        print(f"Teacher recognized! ID: {teacher_id}")
    else:
        print("No teacher recognized.")

    return teacher_id


# ------------------ Test ------------------
if __name__ == "__main__":
    recognized_id = recognize_teacher()
    if recognized_id:
        print("Recognized Teacher ID:", recognized_id)
    else:
        print("Recognition failed.")

