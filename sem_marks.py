from .db_connection import connect_db

def insert_sem_marks(student_id, semester, year, marks_obtained, max_marks):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO SemesterMarks (student_id, semester, year, marks_obtained, max_marks)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, semester, year, marks_obtained, max_marks))
    db.commit()
    db.close()
