import cv2
import face_recognition
import numpy as np
import psycopg2
from datetime import datetime

# Connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="attendance_db",
            user="nevin",  # Replace "nevin" with your PostgreSQL username
            password="keepmecloss",  # Replace "keepmecloss" with your PostgreSQL password
            host="localhost",
            port="5432"
        )
        print("Connected to the database")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# Function to add a new student to the database
def add_student(conn, student_name, roll_number, semester, tutor_name, cgpa, face_encoding):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (student_name, roll_number, semester, tutor_name, cgpa, face_encoding)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_name, roll_number, semester, tutor_name, cgpa, psycopg2.Binary(face_encoding)))
        conn.commit()
        print("Student added successfully")
    except psycopg2.Error as e:
        conn.rollback()
        print("Error adding student to the database:", e)

# Function to record attendance for a student
def record_attendance(conn, student_id, in_full_uniform):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (student_id, in_full_uniform)
            VALUES (%s, %s)
        """, (student_id, in_full_uniform))
        conn.commit()
        print("Attendance recorded successfully")
    except psycopg2.Error as e:
        conn.rollback()
        print("Error recording attendance:", e)

# Function to get attendance records for a student
def get_attendance(conn, student_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT attendance_date, in_full_uniform
            FROM attendance
            WHERE student_id = %s
        """, (student_id,))
        attendance_records = cursor.fetchall()
        return attendance_records
    except psycopg2.Error as e:
        print("Error fetching attendance records:", e)
        return None

# Function to close the database connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Connection closed")

# Function to detect faces and recognize students
def detect_faces_and_recognize_students():
    # Load face recognition model
    known_face_encodings = []
    known_face_names = []
    conn = connect_to_db()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, face_encoding FROM students")
            rows = cursor.fetchall()
            for row in rows:
                student_id, student_name, face_encoding = row
                known_face_encodings.append(np.frombuffer(face_encoding, dtype=np.float64))
                known_face_names.append(student_name)
        except psycopg2.Error as e:
            print("Error fetching student data:", e)
            close_connection(conn)
            return
    
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Check if the student is in full uniform
            in_full_uniform = check_uniform(frame)  # You need to implement this function

            # Record attendance for the student
            if name != "Unknown":
                student_id = rows[first_match_index][0]
                record_attendance(conn, student_id, in_full_uniform)

            # Draw a box around the face
            top, right, bottom, left = face_locations[0]
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    close_connection(conn)

# Function to check if the student is in full uniform
def check_uniform(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Check if the face is detected
        if len(faces) > 0:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Check if the upper body is covered by a uniform color
            # For simplicity, let's assume that the uniform color is blue
            # You can adjust the color range based on the color of the uniform
            roi = frame[y:y+h, x:x+w]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([90, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            res = cv2.bitwise_and(roi, roi, mask=mask)
            percentage_blue = cv2.countNonZero(mask) / (w * h)

            # If more than 10% of the upper body is covered by blue, consider it as full uniform
            if percentage_blue > 0.1:
                return True

    return False

if __name__ == "__main__":
    detect_faces_and_recognize_students()
