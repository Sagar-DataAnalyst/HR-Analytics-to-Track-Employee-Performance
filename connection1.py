import os

import mysql.connector


def main():
    password = os.getenv("MYSQL_PASSWORD")
    if password is None:
        raise SystemExit("Set the MYSQL_PASSWORD environment variable before running.")

    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=password,
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS emp")
            cursor.execute("USE emp")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    position VARCHAR(100) NOT NULL,
                    salary DECIMAL(10, 2) NOT NULL
                )
            """)

        print("Connected to MySQL database successfully!")
        print("Connection ID:", connection.connection_id)
    except mysql.connector.Error as err:
        raise SystemExit(f"Could not initialize the database: {err}") from err
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
