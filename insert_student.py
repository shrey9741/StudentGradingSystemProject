from .db_connection import connect_db

def insert_student(student_id, name, department, year, password):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO Students (student_id, name, department, year, password)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, name, department, year, password))
    db.commit()
    db.close()
