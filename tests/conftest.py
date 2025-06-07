import pyodbc
import pytest

from app.database import get_test_connection
from app.setup_db_test import create_all_tables


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_all_tables()


@pytest.fixture(autouse=True)
def test_db_connection():
    conn = get_test_connection()
    cursor = conn.cursor()

    
    cursor.execute("DELETE FROM Enrollments")
    cursor.execute("DELETE FROM Courses")
    cursor.execute("DELETE FROM Students")

    conn.commit()
    yield conn
    conn.close()
