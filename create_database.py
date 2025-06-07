import pyodbc
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

def create_database(server, database_name):
    try:
        # 
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;'
        with pyodbc.connect(conn_str, autocommit=True) as conn:
            cursor = conn.cursor()
            # 
            cursor.execute(f"SELECT db_id('{database_name}')")
            result = cursor.fetchone()
            if result[0] is None:
                # 
                cursor.execute(f"CREATE DATABASE {database_name}")
                logging.info(f"Database '{database_name}' has been created.")
            else:
                logging.info(f"Databse '{database_name}' already exists.")
    except Exception as e:
        logging.error(f"Error while creating '{database_name}': {e}")

if __name__ == "__main__":
    create_database("localhost", "Application")
    create_database("localhost", "ApplicationTest")
