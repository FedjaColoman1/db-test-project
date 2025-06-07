import pytest
import pyodbc

from app.procedures import proc_add_student, proc_get_student_by_email

def test_add_student_procedure(test_db_connection):
    proc_add_student(test_db_connection) 

    cursor = test_db_connection.cursor()

    cursor.execute("EXEC AddStudent @Name = ?, @Email = ?", ("name", "name@example.com"))
    test_db_connection.commit()

    cursor.execute("SELECT * FROM Students WHERE name = ?", ("name",))
    result = cursor.fetchone()

    assert result is not None
    assert result.name == "name"

def test_add_duplicate_student_procedure_fails(test_db_connection):
    proc_add_student(test_db_connection) 

    cursor = test_db_connection.cursor()

    cursor.execute("EXEC AddStudent @Name = ?, @Email = ?", ("name", "name@example.com"))
    test_db_connection.commit()

    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("EXEC AddStudent @Name = ?, @Email = ?", ("name2", "name@example.com"))
        test_db_connection.commit()

def test_get_student_by_email_procedure(test_db_connection):
    proc_get_student_by_email(test_db_connection)
    cursor = test_db_connection.cursor()

    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", ("Stored Student", "student@test.com"))
    test_db_connection.commit()

    cursor.execute("EXEC GetStudentByEmail @Email = ?", "student@test.com")
    result = cursor.fetchone()

    assert result is not None
    assert result.name == "Stored Student"
    assert result.email == "student@test.com"


def test_add_student_procedure_null_email_fails(test_db_connection):
    cursor = test_db_connection.cursor()
    with pytest.raises(pyodbc.IntegrityError):
        cursor.execute("EXEC AddStudent ?, ?", ("Ime", None))
        test_db_connection.commit()
