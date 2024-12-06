from backend.db_connection import connect_db

def initialize_database():
    connection = connect_db()
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            grade VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            attendance_percentage FLOAT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS semester_marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            semester INT,
            marks FLOAT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
