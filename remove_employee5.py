import os

import mysql.connector


def check_employee(employee_id):
    with con.cursor() as cursor:
        cursor.execute("SELECT 1 FROM employees WHERE id=%s", (employee_id,))
        return cursor.fetchone() is not None


def remove_employee():
    employee_id = input("Enter Employee Id: ")

    try:
        if not check_employee(employee_id):
            print("Employee does not exist. Please try again.")
            return

        with con.cursor() as cursor:
            cursor.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
        con.commit()
        print("Employee Removed Successfully")
    except mysql.connector.Error as err:
        con.rollback()
        print(f"Error: {err}")


if __name__ == "__main__":
    try:
        con = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.environ["MYSQL_PASSWORD"],
            database=os.getenv("MYSQL_DATABASE", "emp"),
        )
    except KeyError:
        raise SystemExit("Set the MYSQL_PASSWORD environment variable before running.")
    except mysql.connector.Error as err:
        raise SystemExit(f"Could not connect to MySQL: {err}") from err

    try:
        remove_employee()
    finally:
        con.close()
