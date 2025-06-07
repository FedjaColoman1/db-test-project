import pyodbc
import logging

from database import get_test_connection
conn = get_test_connection()

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def proc_add_student(conn):
    cursor = conn.cursor()
    create_proc_sql = '''
        IF NOT EXISTS (
            SELECT * FROM sys.objects 
            WHERE type = 'P' AND name = 'AddStudent'
        )
        EXEC('
            CREATE PROCEDURE AddStudent
                @Name NVARCHAR(100),
                @Email NVARCHAR(100)
            AS
            BEGIN
                INSERT INTO Students (name, email)
                VALUES (@Name, @Email)
            END
        ')
    '''
    try:
        cursor.execute(create_proc_sql)
        conn.commit()
        logger.info("Stored procedure 'AddStudent' created or already exists.")
    except Exception as e:
        logger.error(f"Error creating procedure 'AddStudent': {e}")

     
def proc_get_student_by_email(conn):
    cursor = conn.cursor()
    create_proc_sql = '''
        IF NOT EXISTS (
            SELECT * FROM sys.objects 
            WHERE type = 'P' AND name = 'GetStudentByEmail'
        )
        EXEC('
            CREATE PROCEDURE GetStudentByEmail
                @Email NVARCHAR(100)
            AS
            BEGIN
                SELECT StudentID, name, email
                FROM Students
                WHERE email = @Email;
            END
        ')
    '''
    try:
        cursor.execute(create_proc_sql)
        conn.commit()
        logger.info("Stored procedure 'GetStudentByEmail' created or already exists.")
    except Exception as e:
        logger.error(f"Error creating procedure 'GetStudentByEmail': {e}")
