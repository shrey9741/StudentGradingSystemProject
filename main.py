import tkinter as tk
from tkinter import messagebox
from backend.db_connection import connect_db
from backend.insert_student import insert_student
from backend.record_attendance import record_attendance
from backend.sem_marks import insert_sem_marks
from backend.gpa_calculations import calculate_sgpa, calculate_cgpa, calculate_ygpa

def login():
    """Handle the login functionality."""
    username = username_entry.get()
    password = password_entry.get()

    db = connect_db()
    cursor = db.cursor()

    # Admin credentials check
    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Success", "Welcome Admin!")
        open_admin_dashboard()
        return

    # Student login check
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
    dashboard.title("Student Dashboard")
    dashboard.config(bg="#f0f0f0")

    tk.Label(dashboard, text=f"Welcome, {student_id}!", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)

    tk.Button(dashboard, text="Insert Semester Marks", command=lambda: insert_marks(student_id), font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)
    tk.Button(dashboard, text="Record Attendance", command=lambda: record_attendance_gui(student_id), font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)
    tk.Button(dashboard, text="Calculate SGPA", command=lambda: show_sgpa(student_id), font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)
    tk.Button(dashboard, text="Calculate CGPA", command=lambda: show_cgpa(student_id), font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)
    tk.Button(dashboard, text="Calculate YGPA", command=lambda: show_ygpa(student_id), font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)

def open_admin_dashboard():
    """Open the admin dashboard."""
    admin_dashboard = tk.Toplevel(root)
    admin_dashboard.title("Admin Dashboard")
    admin_dashboard.config(bg="#f0f0f0")

    tk.Label(admin_dashboard, text="Admin Dashboard", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)

    tk.Button(admin_dashboard, text="Add New Student", command=open_add_student_form, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)
    tk.Button(admin_dashboard, text="Delete Student", command=open_delete_student_form, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)
    tk.Button(admin_dashboard, text="View All Students", command=view_all_students, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", width=20).pack(pady=5)

def open_add_student_form():
    """Open a form to add a new student."""
    add_form = tk.Toplevel(root)
    add_form.title("Add Student")

    tk.Label(add_form, text="Student ID:", font=("Arial", 12)).pack(pady=5)
    student_id_entry = tk.Entry(add_form, font=("Arial", 12))
    student_id_entry.pack(pady=5)

    tk.Label(add_form, text="Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(add_form, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    tk.Label(add_form, text="Department:", font=("Arial", 12)).pack(pady=5)
    department_entry = tk.Entry(add_form, font=("Arial", 12))
    department_entry.pack(pady=5)

    tk.Label(add_form, text="Year:", font=("Arial", 12)).pack(pady=5)
    year_entry = tk.Entry(add_form, font=("Arial", 12))
    year_entry.pack(pady=5)

    def add_student():
        student_id = student_id_entry.get()
        password = password_entry.get()
        department = department_entry.get()
        year = year_entry.get()

        # Ensure year is an integer
        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid year.")
            return

        try:
            insert_student(student_id, password, department, year)
            messagebox.showinfo("Success", "Student Added Successfully!")
            add_form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")

    tk.Button(add_form, text="Add Student", command=add_student, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").pack(pady=10)

def open_delete_student_form():
    """Open a form to delete a student."""
    delete_form = tk.Toplevel(root)
    delete_form.title("Delete Student")

    tk.Label(delete_form, text="Enter Student ID to Delete:", font=("Arial", 12)).pack(pady=5)
    student_id_entry = tk.Entry(delete_form, font=("Arial", 12))
    student_id_entry.pack(pady=5)

    def delete_student():
        student_id = student_id_entry.get()
        try:
            delete_student_from_db(student_id)
            messagebox.showinfo("Success", f"Student {student_id} Deleted!")
            delete_form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")

    tk.Button(delete_form, text="Delete Student", command=delete_student, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").pack(pady=10)

def delete_student_from_db(student_id):
    """Delete a student from the database."""
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
        db.commit()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {str(e)}")

def view_all_students():
    """View all students in the database."""
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT student_id FROM Students")
        students = cursor.fetchall()
        db.close()

        students_list = "\n".join([student[0] for student in students])
        messagebox.showinfo("All Students", f"Students in the system:\n{students_list}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch students: {str(e)}")

def insert_marks(student_id):
    """Insert semester marks."""
    insert_marks_form = tk.Toplevel(root)
    insert_marks_form.title("Insert Semester Marks")

    tk.Label(insert_marks_form, text="Semester:", font=("Arial", 12)).pack(pady=5)
    semester_entry = tk.Entry(insert_marks_form, font=("Arial", 12))
    semester_entry.pack(pady=5)

    tk.Label(insert_marks_form, text="Year:", font=("Arial", 12)).pack(pady=5)
    year_entry = tk.Entry(insert_marks_form, font=("Arial", 12))
    year_entry.pack(pady=5)

    tk.Label(insert_marks_form, text="Marks Obtained:", font=("Arial", 12)).pack(pady=5)
    marks_obtained_entry = tk.Entry(insert_marks_form, font=("Arial", 12))
    marks_obtained_entry.pack(pady=5)

    tk.Label(insert_marks_form, text="Max Marks:", font=("Arial", 12)).pack(pady=5)
    max_marks_entry = tk.Entry(insert_marks_form, font=("Arial", 12))
    max_marks_entry.pack(pady=5)

    def insert():
        semester = semester_entry.get()
        year = year_entry.get()
        marks_obtained = marks_obtained_entry.get()
        max_marks = max_marks_entry.get()

        try:
            semester = int(semester)
            year = int(year)
            marks_obtained = int(marks_obtained)
            max_marks = int(max_marks)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid marks and semester/year.")
            return

        try:
            insert_sem_marks(student_id, semester, year, marks_obtained, max_marks)
            messagebox.showinfo("Success", "Semester Marks Inserted Successfully!")
            insert_marks_form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert marks: {str(e)}")

    tk.Button(insert_marks_form, text="Insert Marks", command=insert, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").pack(pady=10)

def record_attendance_gui(student_id):
    """Record attendance."""
    record_attendance_form = tk.Toplevel(root)
    record_attendance_form.title("Record Attendance")

    tk.Label(record_attendance_form, text="Attendance Percentage:", font=("Arial", 12)).pack(pady=5)
    attendance_entry = tk.Entry(record_attendance_form, font=("Arial", 12))
    attendance_entry.pack(pady=5)

    def record():
        try:
            attendance = float(attendance_entry.get())
            if 0 <= attendance <= 100:
                record_attendance(student_id, attendance)
                messagebox.showinfo("Success", "Attendance Recorded Successfully!")
                record_attendance_form.destroy()
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid attendance percentage (0-100).")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for attendance.")

    tk.Button(record_attendance_form, text="Record Attendance", command=record, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").pack(pady=10)

def show_sgpa(student_id):
    """Display SGPA."""
    sgpa_form = tk.Toplevel(root)
    sgpa_form.title("SGPA")

    tk.Label(sgpa_form, text="Enter Semester (e.g., 1, 2, 3):", font=("Arial", 12)).pack(pady=5)
    semester_entry = tk.Entry(sgpa_form, font=("Arial", 12))
    semester_entry.pack(pady=5)

    def calculate():
        try:
            semester = int(semester_entry.get())
            sgpa = calculate_sgpa(student_id, semester)
            messagebox.showinfo("SGPA", f"Your SGPA for semester {semester} is {sgpa}")
            sgpa_form.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid semester number.")

    tk.Button(sgpa_form, text="Calculate SGPA", command=calculate, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").pack(pady=10)

def show_cgpa(student_id):
    """Display CGPA."""
    cgpa = calculate_cgpa(student_id)
    messagebox.showinfo("CGPA", f"Your CGPA is {cgpa}")

def show_ygpa(student_id):
    """Display YGPA."""
    ygpa_form = tk.Toplevel(root)
    ygpa_form.title("YGPA")

    tk.Label(ygpa_form, text="Enter Year (e.g., 1, 2, 3):", font=("Arial", 12)).pack(pady=5)
    year_entry = tk.Entry(ygpa_form, font=("Arial", 12))
    year_entry.pack(pady=5)

    def calculate():
        try:
            year = int(year_entry.get())
            ygpa = calculate_ygpa(student_id, year)
            messagebox.showinfo("YGPA", f"Your YGPA for year {year} is {ygpa}")
            ygpa_form.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid year number.")

    tk.Button(ygpa_form, text="Calculate YGPA", command=calculate, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").pack(pady=10)

# Tkinter GUI
root = tk.Tk()
root.title("Student Grading System Login")
root.config(bg="#f0f0f0")

# Styling for the Login Form
tk.Label(root, text="Student ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Login", command=login, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid").grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
