import pyodbc
import logging
from database import get_test_connection

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

conn = get_test_connection()

def add_student(conn, name, email):
    try:
        if not name or not name.strip():
            raise ValueError("Name must not be empty.")
        if '@' not in email or not email.strip():
            raise ValueError("Invalid email address.")
        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Students(name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        logging.info(f"Added student: {name} ({email})")
    except ValueError as ve:
        logging.warning(f"Validation error while adding student: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error adding student {name}: {e}")


def add_course(conn, name, credits):
    try:
        if not name or not name.strip():
            raise ValueError("Course name must not be empty.")
        if not isinstance(credits, int) or credits <= 0:
            raise ValueError("Credits must be a positive integer.")

        cursor = conn.cursor()
        cursor.execute('INSERT INTO Courses(name, credits) VALUES (?, ?)', (name, credits))
        conn.commit()
        logging.info(f"Added course: {name} with credits {credits}")
    except ValueError as ve:
        logging.warning(f"Validation error while adding course: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error adding course {name}: {e}")


def get_all_students(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Students')
        results = cursor.fetchall()
        logging.info(f"Fetched all students, count: {len(results)}")
        return results
    except Exception as e:
        logging.error(f"Error fetching students: {e}")
        return []

def update_student_email(conn, student_id, new_email):
    try:
        if '@' not in new_email or not new_email.strip():
            raise ValueError("Invalid email address.")

        cursor = conn.cursor()
        cursor.execute('UPDATE Students SET email = ? WHERE StudentID = ?', (new_email, student_id))
        conn.commit()
        logging.info(f"Updated email for student ID {student_id} to {new_email}")
    except ValueError as ve:
        logging.warning(f"Validation error while updating email: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error updating email for student ID {student_id}: {e}")


def delete_student(conn, student_id):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Students WHERE StudentID = ?', (student_id,))
        conn.commit()
        logging.info(f"Deleted student ID {student_id}")
    except Exception as e:
        logging.error(f"Error deleting student ID {student_id}: {e}")

def enroll_student(conn, student_id, course_id):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Enrollments(StudentID, CourseID) VALUES (?, ?)', (student_id, course_id))
        conn.commit()
        logging.info(f"Enrolled student ID {student_id} in course ID {course_id}")
    except Exception as e:
        logging.error(f"Error enrolling student ID {student_id} in course ID {course_id}: {e}")

def get_student_enrollments(conn, student_id):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Enrollments WHERE StudentID = ?', (student_id,))
        results = cursor.fetchall()
        logging.info(f"Fetched enrollments for student ID {student_id}, count: {len(results)}")
        return results
    except Exception as e:
        logging.error(f"Error fetching enrollments for student ID {student_id}: {e}")
        return []

def update_enrollment(conn, student_id, old_course_id, new_course_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE Enrollments SET CourseID = ? WHERE StudentID = ? AND CourseID = ?',
            (new_course_id, student_id, old_course_id)
        )
        conn.commit()
        logging.info(f"Updated enrollment for student ID {student_id} from course ID {old_course_id} to {new_course_id}")
    except Exception as e:
        logging.error(f"Error updating enrollment for student ID {student_id}: {e}")

def delete_enrollment(conn, student_id, course_id):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Enrollments WHERE StudentID = ? AND CourseID = ?', (student_id, course_id))
        conn.commit()
        logging.info(f"Deleted enrollment of student ID {student_id} from course ID {course_id}")
    except Exception as e:
        logging.error(f"Error deleting enrollment for student ID {student_id}: {e}")

def get_all_courses(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Courses')
        results = cursor.fetchall()
        logging.info(f"Fetched all courses, count: {len(results)}")
        return results
    except Exception as e:
        logging.error(f"Error fetching courses: {e}")
        return []

def update_course_name(conn, course_id, new_credits):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Courses SET credits = ? WHERE CourseID = ?",
            (new_credits, course_id)
        )
        conn.commit()
        logging.info(f"Updated course ID {course_id} with new credits {new_credits}")
    except Exception as e:
        logging.error(f"Error updating course ID {course_id}: {e}")

def delete_course(conn, course_id):
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Courses WHERE CourseID = ?', (course_id,))
        conn.commit()
        logging.info(f"Deleted course ID {course_id}")
    except Exception as e:
        logging.error(f"Error deleting course ID {course_id}: {e}")
