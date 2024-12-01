import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",      # Change to your MySQL host
        user="root",           # Change to your MySQL username
        password="Shreykr12#",   # Change to your MySQL password
        database="StudentGradingSystemProject"  # Change to your database name
    )

