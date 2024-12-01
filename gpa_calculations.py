from .db_connection import connect_db

def calculate_sgpa(student_id, semester):
    db = connect_db()
    cursor = db.cursor()
    query = """
        SELECT marks_obtained, max_marks FROM SemesterMarks
        WHERE student_id = %s AND semester = %s
    """
    cursor.execute(query, (student_id, semester))
    results = cursor.fetchall()
    
    total_marks = sum(marks for marks, _ in results)
    total_max_marks = sum(max_marks for _, max_marks in results)
    db.close()
    return round((total_marks / total_max_marks) * 10, 2) if total_max_marks else 0

def calculate_cgpa(student_id):
    db = connect_db()
    cursor = db.cursor()
    query = """
        SELECT marks_obtained, max_marks FROM SemesterMarks
        WHERE student_id = %s
    """
    cursor.execute(query, (student_id,))
    results = cursor.fetchall()
    
    total_marks = sum(marks for marks, _ in results)
    total_max_marks = sum(max_marks for _, max_marks in results)
    db.close()
    return round((total_marks / total_max_marks) * 10, 2) if total_max_marks else 0

def calculate_ygpa(student_id, year):
    db = connect_db()
    cursor = db.cursor()
    query = """
        SELECT marks_obtained, max_marks FROM SemesterMarks
        WHERE student_id = %s AND year = %s
    """
    cursor.execute(query, (student_id, year))
    results = cursor.fetchall()
    
    total_marks = sum(marks for marks, _ in results)
    total_max_marks = sum(max_marks for _, max_marks in results)
    db.close()
    return round((total_marks / total_max_marks) * 10, 2) if total_max_marks else 0
