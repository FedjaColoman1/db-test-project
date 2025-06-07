import pytest
import pyodbc
from app.operations import add_course, get_all_courses, update_course_name, delete_course

def test_addCourse(test_db_connection):
    add_course(test_db_connection, "Test Ime", 1234)
    cursor = test_db_connection.cursor()
    cursor.execute("SELECT * FROM Courses WHERE name = ?", ("Test Ime",))
    result = cursor.fetchone()
    assert result is not None

def test_get_all_courses(test_db_connection):
    add_course(test_db_connection, "Test Ime", 1234)
    students = get_all_courses(test_db_connection)
    assert any(c.name == "Test Ime" for c in students)

def test_update_course_name(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", ("Test Ime", 123))
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC")
    course_id = cursor.fetchone()[0]

    update_course_name(test_db_connection, course_id, 111 )
    cursor.execute("SELECT * FROM Courses WHERE CourseId = ? AND credits = ?", (course_id, 111))
    result = cursor.fetchone()
    assert result is not None

def test_delete_course(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Courses (name, credits) VALUES (?, ?)", ("Test Ime", 123))
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 CourseID FROM Courses ORDER BY CourseID DESC")
    course_id = cursor.fetchone()[0]

    delete_course(test_db_connection, course_id)
    cursor.execute("SELECT * FROM Courses WHERE CourseId = ?", (course_id))
    result = cursor.fetchone()
    assert result is None

def test_add_course_empty_name_raises_value_error(test_db_connection):
    with pytest.raises(ValueError, match="Course name must not be empty"):
        add_course(test_db_connection, "", 3)

def test_add_course_invalid_credits_raises_value_error(test_db_connection):
    with pytest.raises(ValueError, match="Credits must be a positive integer"):
        add_course(test_db_connection, "Physics", -2)
