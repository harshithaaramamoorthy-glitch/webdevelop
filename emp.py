import mysql.connector

def get_database_connection():
        return mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="harshithaa@99",
        database="employeedb"
    )