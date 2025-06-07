import pyodbc
import pytest

def test_student_name_not_null(test_db_connection):
    cursor = test_db_connection.cursor()
    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (None, "email@test.com"))
        test_db_connection.commit()
    cursor.close()

def test_student_name_email_unique(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("name1", "email@test.com"))
    test_db_connection.commit()
    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("name2", "email@test.com"))
        test_db_connection.commit()
    cursor.close()

def test_course_name_not_null(test_db_connection):
    cursor = test_db_connection.cursor()
    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", (None, 123))
        test_db_connection.commit()
    cursor.close()

def test_course_credits_check(test_db_connection):
    cursor = test_db_connection.cursor()
    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", ("course", 0))
        test_db_connection.commit()
    cursor.close()

def test_enrollment_foreign_key_violation(test_db_connection):
    cursor = test_db_connection.cursor()
    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("INSERT INTO Enrollments (StudentID, CourseID) VALUES (?, ?)", (999, 999))
        test_db_connection.commit()
    cursor.close()



    