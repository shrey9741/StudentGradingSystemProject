from .db_connection import connect_db

def record_attendance(student_id, attendance_percentage):
    """Record attendance for a student."""
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO Attendance (student_id, attendance_percentage)
        VALUES (%s, %s)
    """
    cursor.execute(query, (student_id, attendance_percentage))
    db.commit()
    db.close()

def get_attendance(student_id):
    """Retrieve the attendance percentage for a student."""
    db = connect_db()
    cursor = db.cursor()
    query = """
        SELECT attendance_percentage FROM Attendance WHERE student_id = %s
    """
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    db.close()
    
    if result:
        return result[0]  # Return the attendance percentage
    else:
        return None  # Return None if no attendance data is found for the student
