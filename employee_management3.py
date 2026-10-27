import os
from decimal import Decimal, InvalidOperation

import mysql.connector


def check_employee(employee_id):
    with con.cursor() as cursor:
        cursor.execute("SELECT 1 FROM employees WHERE id=%s", (employee_id,))
        return cursor.fetchone() is not None


def add_employee():
    employee_id = input("Enter Employee Id: ")
    if check_employee(employee_id):
        print("Employee already exists. Please try again.")
        return

    name = input("Enter Employee Name: ")
    position = input("Enter Employee Post: ")
    salary = input("Enter Employee Salary: ")

    try:
        with con.cursor() as cursor:
            cursor.execute(
                "INSERT INTO employees (id, name, position, salary) "
                "VALUES (%s, %s, %s, %s)",
                (employee_id, name, position, salary),
            )
        con.commit()
        print("Employee Added Successfully")
    except mysql.connector.Error as err:
        con.rollback()
        print(f"Error: {err}")


def remove_employee():
    employee_id = input("Enter Employee Id: ")
    if not check_employee(employee_id):
        print("Employee does not exist. Please try again.")
        return

    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
        con.commit()
        print("Employee Removed Successfully")
    except mysql.connector.Error as err:
        con.rollback()
        print(f"Error: {err}")


def promote_employee():
    employee_id = input("Enter Employee's Id: ")
    if not check_employee(employee_id):
        print("Employee does not exist. Please try again.")
        return

    try:
        amount = Decimal(input("Enter increase in Salary: "))
        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE employees SET salary=salary+%s WHERE id=%s",
                (amount, employee_id),
            )
        con.commit()
        print("Employee Promoted Successfully")
    except (InvalidOperation, mysql.connector.Error) as err:
        con.rollback()
        print(f"Error: {err}")


def display_employees():
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()

        for employee in employees:
            print("Employee Id : ", employee[0])
            print("Employee Name : ", employee[1])
            print("Employee Post : ", employee[2])
            print("Employee Salary : ", employee[3])
            print("------------------------------------")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def menu():
    while True:
        print("\nWelcome to Employee Management Record")
        print("Press:")
        print("1 to Add Employee")
        print("2 to Remove Employee")
        print("3 to Promote Employee")
        print("4 to Display Employees")
        print("5 to Exit")

        choice = input("Enter your Choice: ")
        if choice == "1":
            add_employee()
        elif choice == "2":
            remove_employee()
        elif choice == "3":
            promote_employee()
        elif choice == "4":
            display_employees()
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid Choice! Please try again.")


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
        menu()
    finally:
        con.close()
