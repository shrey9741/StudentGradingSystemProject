import tkinter as tk
from tkinter import messagebox

from backend.db_connection import connect_db
from backend.insert_student import insert_student
from backend.record_attendance import record_attendance
from backend.sem_marks import insert_sem_marks
from backend.gpa_calculations import calculate_sgpa, calculate_cgpa, calculate_ygpa

from backend.grade_card import generate_grade_card


def login():
    """Handle the login functionality."""
    username = username_entry.get()
    password = password_entry.get()
    
    db = connect_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM Students WHERE student_id = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    db.close()
    
    if result:
        messagebox.showinfo("Login Success", "Welcome to the Student Grading System!")
        open_dashboard(username)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

def open_dashboard(student_id):
    """Open the dashboard for the student."""
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    
    tk.Label(dashboard, text=f"Welcome, {student_id}!", font=("Arial", 16)).pack(pady=20)
    
    tk.Button(dashboard, text="Insert Semester Marks", command=lambda: insert_marks(student_id)).pack(pady=5)
    tk.Button(dashboard, text="Record Attendance", command=lambda: record_attendance_gui(student_id)).pack(pady=5)
    tk.Button(dashboard, text="Calculate SGPA", command=lambda: show_sgpa(student_id)).pack(pady=5)
    tk.Button(dashboard, text="Calculate CGPA", command=lambda: show_cgpa(student_id)).pack(pady=5)
    tk.Button(dashboard, text="Calculate YGPA", command=lambda: show_ygpa(student_id)).pack(pady=5)

def insert_marks(student_id):
    """Insert semester marks."""
    semester = int(input("Enter Semester: "))
    year = int(input("Enter Year: "))
    marks_obtained = int(input("Enter Marks Obtained: "))
    max_marks = int(input("Enter Max Marks: "))
    
    insert_sem_marks(student_id, semester, year, marks_obtained, max_marks)
    messagebox.showinfo("Success", "Semester Marks Inserted Successfully!")

def record_attendance_gui(student_id):
    """Record attendance."""
    attendance = float(input("Enter Attendance Percentage: "))
    record_attendance(student_id, attendance)
    messagebox.showinfo("Success", "Attendance Recorded Successfully!")

def show_sgpa(student_id):
    """Display SGPA."""
    semester = int(input("Enter Semester (e.g., 1, 2, 3): "))
    sgpa = calculate_sgpa(student_id, semester)
    messagebox.showinfo("SGPA", f"Your SGPA for semester {semester} is {sgpa}")

def show_cgpa(student_id):
    """Display CGPA."""
    cgpa = calculate_cgpa(student_id)
    messagebox.showinfo("CGPA", f"Your CGPA is {cgpa}")

def show_ygpa(student_id):
    """Display YGPA."""
    year = int(input("Enter Year (e.g., 1, 2, 3): "))
    ygpa = calculate_ygpa(student_id, year)
    messagebox.showinfo("YGPA", f"Your YGPA for year {year} is {ygpa}")


# Tkinter GUI
root = tk.Tk()
root.title("Student Grading System Login")

tk.Label(root, text="Student ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
