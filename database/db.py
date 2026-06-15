import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Siddu@2005",
        database="railway_management"
    )
    return connection