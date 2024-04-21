import psycopg2
from psycopg2 import sql

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
def add_student(conn, student_name, roll_number, semester, tutor_name, cgpa):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (student_name, roll_number, semester, tutor_name, cgpa)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_name, roll_number, semester, tutor_name, cgpa))
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

# Close the database connection
def close_connection(conn):
    if conn is not None:
        conn.close()
        print("Connection closed")

# Example usage
if __name__ == "__main__":
    conn = connect_to_db()
    if conn is not None:
        # Add a new student
        add_student(conn, "John Doe", "12345", "Semester 1", "Dr. Smith", 8.5)
        
        # Record attendance for the student
        student_id = 1  # Assuming the student ID is 1
        in_full_uniform = True  # Assuming the student is in full uniform
        record_attendance(conn, student_id, in_full_uniform)
        
        # Get attendance records for the student
        attendance_records = get_attendance(conn, student_id)
        print("Attendance records:", attendance_records)
        
        # Close the connection
        close_connection(conn)
