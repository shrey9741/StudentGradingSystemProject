from .db_connection import connect_db

def record_attendance(student_id, attendance_percentage):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO Attendance (student_id, attendance_percentage)
        VALUES (%s, %s)
    """
    cursor.execute(query, (student_id, attendance_percentage))
    db.commit()
    db.close()
