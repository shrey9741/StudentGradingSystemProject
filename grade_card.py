from .gpa_calculations import calculate_sgpa, calculate_cgpa, calculate_ygpa
from backend.record_attendance import record_attendance, get_attendance


def generate_grade_card(student_id, year=1, attendance_percentage=None):
    """
    Generates a grade card for a student.
    
    Args:
        student_id (str): The ID of the student.
        year (int): The academic year. Defaults to 1.
        attendance_percentage (float, optional): Attendance percentage to be recorded.
    
    Returns:
        dict: A dictionary containing the grade card details.
    """
    # Calculate SGPA, CGPA, and YGPA
    sgpa = calculate_sgpa(student_id, semester=1)  # Example semester
    cgpa = calculate_cgpa(student_id)
    ygpa = calculate_ygpa(student_id, year)
    
    # Record attendance if provided
    if attendance_percentage is not None:
        record_attendance(student_id, attendance_percentage)
    
    # Retrieve attendance from the database
    attendance = get_attendance(student_id)

    # Generate the grade card
    grade_card = {
        "SGPA": sgpa,
        "CGPA": cgpa,
        "YGPA": ygpa,
        "Attendance": f"{attendance}%",
        "Performance": (
            "Fast Learner" if attendance >= 70
            else "Average Learner" if 40 <= attendance < 70
            else "Slow Learner"
        ),
    }
    
    return grade_card
