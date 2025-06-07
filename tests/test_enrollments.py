import pytest
import pyodbc
from app.operations import add_student, add_course, enroll_student, get_student_enrollments, update_enrollment, delete_enrollment

def test_enroll_student(test_db_connection):
    cursor = test_db_connection.cursor()

    add_student(test_db_connection, "Test Ime", "test@email.com")
    test_db_connection.commit()
    add_course(test_db_connection, "Test Ime", 1234)
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC")
    student_id = cursor.fetchone()[0]

    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC")
    course_id = cursor.fetchone()[0]

    enroll_student(test_db_connection, student_id, course_id)
    cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ? AND CourseID = ?", (student_id, course_id))
    result = cursor.fetchone()
    assert result is not None

def test_get_student_enrollments(test_db_connection):
    cursor = test_db_connection.cursor()

    add_student(test_db_connection, "Test Ime", "test@email.com")
    add_course(test_db_connection, "Test Kurs", 5)
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC")
    student_id = cursor.fetchone()[0]

    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC")
    course_id = cursor.fetchone()[0]

    enroll_student(test_db_connection, student_id, course_id)
    test_db_connection.commit()

    enrollments = get_student_enrollments(test_db_connection, student_id)
    assert any(enr[1] == course_id for enr in enrollments)



def test_update_enrollment(test_db_connection):
    cursor = test_db_connection.cursor()
    
    add_student(test_db_connection, "Test Ime", "test@email.com")
    add_course(test_db_connection, "Stari Kurs", 3)
    add_course(test_db_connection, "Novi Kurs", 5)
    test_db_connection.commit()
    
    cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC")
    student_id = cursor.fetchone()[0]
    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID ASC")
    old_course_id = cursor.fetchone()[0]
    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC")
    new_course_id = cursor.fetchone()[0]
    
    enroll_student(test_db_connection, student_id, old_course_id)
    update_enrollment(test_db_connection, student_id, old_course_id, new_course_id)
    
    cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ? AND CourseID = ?", (student_id, new_course_id))
    result = cursor.fetchone()
    assert result is not None


def test_delete_enrollment(test_db_connection):
    cursor = test_db_connection.cursor()

    add_student(test_db_connection, "Test Ime", "test@email.com")
    add_course(test_db_connection, "Test Kurs", 3)
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC")
    student_id = cursor.fetchone()[0]
    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC")
    course_id = cursor.fetchone()[0]

    enroll_student(test_db_connection, student_id, course_id)
    delete_enrollment(test_db_connection, student_id, course_id)

    cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ? AND CourseID = ?", (student_id, course_id))
    result = cursor.fetchone()
    assert result is None

def test_delete_student_cascades_enrollments(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("Student", "email1"))
    student_id = cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC").fetchone()[0]
    cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", ("Math", 5))
    course_id = cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC").fetchone()[0]
    cursor.execute("INSERT INTO Enrollments (studentID, courseID) VALUES (?, ?)", (student_id, course_id))
    test_db_connection.commit()

    cursor.execute("DELETE FROM Students WHERE StudentID = ?", (student_id,))
    test_db_connection.commit()

    cursor.execute("SELECT * FROM Enrollments WHERE StudentID = ?", (student_id,))
    assert cursor.fetchone() is None


def test_duplicate_enrollment_not_allowed(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("Student", "email1"))
    student_id = cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC").fetchone()[0]
    cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", ("Math", 5))
    course_id = cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC").fetchone()[0]
    cursor.execute("INSERT INTO Enrollments (studentID, courseID) VALUES (?, ?)", (student_id, course_id))
    test_db_connection.commit()

    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("INSERT INTO Enrollments (studentID, courseID) VALUES (?, ?)", (student_id, course_id))
        test_db_connection.commit()
    cursor.close()

def test_student_course_join_query(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("Ana", "ana@test.com"))
    student_id = cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC").fetchone()[0]
    cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", ("Biology", 5))
    course_id = cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC").fetchone()[0]
    cursor.execute("INSERT INTO Enrollments (studentID, courseID) VALUES (?, ?)", (student_id, course_id))
    test_db_connection.commit()

    cursor.execute('''
        SELECT Students.name, Courses.name
        FROM Enrollments
        JOIN Students ON Enrollments.StudentID = Students.StudentID
        JOIN Courses ON Enrollments.CourseID = Courses.CourseID
    ''')
    result = cursor.fetchone()
    assert result[0] == "Ana"
    assert result[1] == "Biology"