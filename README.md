# Database Testing with Python and SQL Server
This project demonstrates how to test a relational database using Python tools such as `pytest`, `pyodbc`, and `pytest-cov`. It focuses on applying unit and integration testing techniques to a Microsoft SQL Server database that handles students, courses, and enrollments.
A separate test database is automatically created and used to ensure data isolation and safe testing. The goal is to show practical usage of automated database testing in real-world scenarios.

## Tech Stack
- **Programming Language**: Python 3.11  
- **Database**: Microsoft SQL Server  
- **Database Driver**: `pyodbc`  
- **Testing Framework**: `pytest`  
- **Test Coverage Tool**: `pytest-cov`  
- **Logging**: Python `logging` module  

## Project Structure

```text
db_test_project/
├── app/
│   ├── database.py               # Functions for connecting to production and test databases
│   ├── operations.py             # CRUD operations for students, courses, and enrollments
│   ├── procedures.py             # Stored procedure execution functions
│   ├── setup_db_prod.py          # Creates tables and constraints in the production database
│   └── setup_db_test.py          # Creates tables and constraints in the test database
│
├── tests/
│   ├── conftest.py               # Pytest fixtures for test database setup
│   ├── test_students.py          # Tests for student-related operations
│   ├── test_courses.py           # Tests for course-related operations
│   ├── test_enrollments.py       # Tests for enrollments
│   ├── test_procedures.py        # Tests for stored procedures
│   └── test_constraints.py       # Tests for database constraints and validations
│
├── create_database.py           # Script to create production and test databases via connection to master
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview and instructions
```

## Installation
1. Clone the repository:
git clone https://github.com/FedjaColoman1/db_test_project.git
cd db_test_project

2. Create a virtual environment (optional but recommended):
python -m venv venv
venv\Scripts\activate  # On Windows

3. Install required dependencies:
pip install -r requirements.txt

4. Ensure SQL Server is running and accessible.
You must have:
SQL Server installed and running locally (or accessible remotely)
The ODBC Driver 17 (or newer) for SQL Server installed

5. Create databases (Production and Test):
Run the following script to create both databases automatically:
python create_database.py

6. Set up database schema (tables, constraints, procedures):
python app/setup_db_prod.py
python app/setup_db_test.py

## Usage
Running Tests
To run the automated database tests:
pytest

Make sure your SQL Server service is running and that the test database exists or can be created by the create_database.py script.

## License
This project is currently unlicensed. All rights reserved.
You may view and use the code for educational purposes, but redistribution or commercial use is not permitted without permission.
