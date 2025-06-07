import pyodbc

def get_connection():
    return pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=Application;'  
    'Trusted_Connection=yes;'
)

def get_test_connection():
    return pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=ApplicationTest;'  
    'Trusted_Connection=yes;'
)