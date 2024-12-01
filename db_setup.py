from db_connection import connect_db
# Importing functions and classes from backend modules



def initialize_database():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(50),
            year INT,
            password VARCHAR(64)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            student_id VARCHAR(10),
            attendance_percentage FLOAT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SemesterMarks (
            student_id VARCHAR(10),
            semester INT,
            year INT,
            marks_obtained FLOAT,
            max_marks FLOAT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    """)

    db.commit()
    db.close()
