import pyodbc

from database import get_connection

connection = get_connection()
cursor = connection.cursor()
def create_Students_table():
        cursor.execute('''
            CREATE TABLE Students(
                StudentId INT IDENTITY(1, 1) PRIMARY KEY,
                name VARCHAR(32),
                email VARCHAR(128))
    ''')

def create_Courses_table():
        cursor.execute('''
CREATE TABLE Courses(
    CourseId INT IDENTITY(1, 1) PRIMARY KEY,
    name VARCHAR(32),
    credits INT)
''')

def create_Enrollments_table():
        cursor.execute('''
CREATE TABLE Enrollments(
    StudentID INT,
    CourseId INT,
    EnrolledOn DATE
    FOREIGN KEY (StudentID) REFERENCES Students(StudentId),
    FOREIGN KEY (CourseId) REFERENCES Courses(CourseId))           
''')