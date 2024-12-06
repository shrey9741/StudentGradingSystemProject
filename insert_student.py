from .db_connection import connect_db

def insert_student(student_id, name, department, year, password):
    """
    Insert a new student into the Students table.

    Parameters:
        student_id (str): The ID of the student.
        name (str): The name of the student.
        department (str): The department of the student.
        year (int): The year of the student.
        password (str): The password for the student.
    """
    try:
        # Connect to the database
        db = connect_db()
        cursor = db.cursor()

        # SQL query to insert a new student record
        query = """
            INSERT INTO Students (student_id, name, department, year, password)
            VALUES (%s, %s, %s, %s, %s)
        """

        # Execute the query with the provided parameters
        cursor.execute(query, (student_id, name, department, year, password))

        # Commit the changes to the database
        db.commit()

        print("Student added successfully!")
    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error inserting student: {e}")
    finally:
        # Close the database connection
        if db:
            db.close()

# Example of a fixed function call (if needed in your GUI or main code)
def add_student_from_gui():
    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    department = input("Enter Department: ")
    year = input("Enter Year: ")
    password = input("Enter Password: ")

    try:
        # Ensure year is an integer
        year = int(year)

        # Call the function with all required arguments
        insert_student(student_id, name, department, year, password)

        print("Student added successfully!")
    except ValueError:
        print("Invalid input: Year must be an integer.")
    except Exception as e:
        print(f"Error: {e}")
