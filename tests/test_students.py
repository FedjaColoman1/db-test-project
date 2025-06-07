import pytest
import pyodbc
from app.operations import add_student, get_all_students, update_student_email, delete_student

def test_add_student(test_db_connection):
    add_student(test_db_connection, "Test Ime", "test@email.com")
    cursor = test_db_connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE name = ?", ("Test Ime",))
    result = cursor.fetchone()
    assert result is not None

def test_get_all_students(test_db_connection):
    add_student(test_db_connection, "Test Ime", "test@email.com")
    students = get_all_students(test_db_connection)
    assert any(s.name == "Test Ime" for s in students)

def test_update_student_email(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("Test Ime", "test@email.com"))
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC")
    student_id = cursor.fetchone()[0]

    update_student_email(test_db_connection, student_id, "newemail@email.com")
    cursor.execute("SELECT * FROM Students WHERE StudentId = ? AND email = ?", (student_id, "newemail@email.com"))
    result = cursor.fetchone()
    assert result is not None

def test_delete_student(test_db_connection):
    cursor = test_db_connection.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("Test Ime", "test@email.com"))
    test_db_connection.commit()

    cursor.execute("SELECT TOP 1 StudentID FROM Students ORDER BY StudentID DESC")
    student_id = cursor.fetchone()[0]

    delete_student(test_db_connection, student_id)
    cursor.execute("SELECT * FROM Students WHERE StudentId = ?", (student_id,))
    result = cursor.fetchone()
    assert result is None

def test_add_student_empty_name_raises_value_error(test_db_connection):
    with pytest.raises(ValueError, match="Name must not be empty"):
        add_student(test_db_connection, "", "test@example.com")

def test_add_student_invalid_email_raises_value_error(test_db_connection):
    with pytest.raises(ValueError, match="Invalid email address"):
        add_student(test_db_connection, "John", "invalidemail.com")

def test_update_student_email_invalid_email_raises_value_error(test_db_connection):
    with pytest.raises(ValueError, match="Invalid email address"):
        update_student_email(test_db_connection, 1, "bademail")

