def add_employee():
    employee_id = input("Enter Employee Id: ")

    if check_employee(employee_id):
        print("Employee already exists. Please try again.")
        return

    name = input("Enter Employee Name: ")
    position = input("Enter Employee Post: ")
    salary = input("Enter Employee Salary: ")

    sql = (
        "INSERT INTO employees (id, name, position, salary) "
        "VALUES (%s, %s, %s, %s)"
    )
    data = (employee_id, name, position, salary)
    cursor = con.cursor()

    try:
        cursor.execute(sql, data)
        con.commit()
        print("Employee Added Successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()
    finally:
        cursor.close()
