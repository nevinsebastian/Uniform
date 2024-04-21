import cv2
import face_recognition
import numpy as np
import psycopg2

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

# Function to close the database connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Connection closed")

# Function to capture student's face and register them
def register_student():
    student_name = input("Enter student's name: ")
    roll_number = input("Enter student's roll number: ")
    semester = input("Enter student's semester: ")
    tutor_name = input("Enter student's tutor name: ")
    cgpa = input("Enter student's CGPA: ")

    # Connect to the database
    conn = connect_to_db()
    if conn is not None:
        try:
            # Load the webcam
            cap = cv2.VideoCapture(0)

            while True:
                ret, frame = cap.read()
                rgb_frame = frame[:, :, ::-1]

                # Detect face locations
                face_locations = face_recognition.face_locations(rgb_frame)

                if len(face_locations) > 0:
                    for top, right, bottom, left in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    cv2.imshow('Register Student', frame)

                    # Capture student's face
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        # Encode the face
                        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                        
                        # Add the student to the database
                        add_student(conn, student_name, roll_number, semester, tutor_name, cgpa, face_encoding)
                        break

                    # Exit the loop
                    elif cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("No face detected. Please make sure your face is properly visible.")

            # Release the webcam and close the window
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print("Error:", e)
            close_connection(conn)

        # Close the database connection
        close_connection(conn)

if __name__ == "__main__":
    register_student()
