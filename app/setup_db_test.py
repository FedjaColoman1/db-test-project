import logging
from app.database import get_test_connection

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CreateTables:
    @staticmethod
    def create_students_table(cursor):
        try:
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Students' AND xtype='U')
                CREATE TABLE Students (
                    StudentId INT IDENTITY(1, 1) PRIMARY KEY,
                    name VARCHAR(32) NOT NULL,
                    email VARCHAR(128) UNIQUE NOT NULL
                )
            ''')
            logger.info("Table 'Students' created or already exists.")
        except Exception as e:
            logger.error(f"Error creating 'Students' table: {e}")

    @staticmethod
    def create_courses_table(cursor):
        try:
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Courses' AND xtype='U')
                CREATE TABLE Courses (
                    CourseId INT IDENTITY(1, 1) PRIMARY KEY,
                    name VARCHAR(32) NOT NULL,
                    credits INT CHECK (credits > 0)
                )
            ''')
            logger.info("Table 'Courses' created or already exists.")
        except Exception as e:
            logger.error(f"Error creating 'Courses' table: {e}")

    @staticmethod
    def create_enrollments_table(cursor):
        try:
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Enrollments' AND xtype='U')
                CREATE TABLE Enrollments (
                    StudentID INT,
                    CourseID INT,
                    EnrolledOn DATE DEFAULT GETDATE(),
                    CONSTRAINT FK_Student FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
                    CONSTRAINT FK_Course FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                    CONSTRAINT UQ_Student_Course UNIQUE (StudentID, CourseID)
                )
            ''')
            logger.info("Table 'Enrollments' created or already exists.")
        except Exception as e:
            logger.error(f"Error creating 'Enrollments' table: {e}")

def create_all_tables():
    try:
        connection = get_test_connection()
        cursor = connection.cursor()

        CreateTables.create_students_table(cursor)
        CreateTables.create_courses_table(cursor)
        CreateTables.create_enrollments_table(cursor)

        connection.commit()
        logger.info("All tables created and committed successfully.")

    except Exception as e:
        logger.error(f"Error during table creation: {e}")

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

if __name__ == "__main__":
    create_all_tables()
