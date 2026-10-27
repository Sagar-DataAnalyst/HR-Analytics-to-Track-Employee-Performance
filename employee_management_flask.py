import os
import secrets
from decimal import Decimal, InvalidOperation

import mysql.connector
from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)
MAX_SALARY = Decimal("99999999.99")


def get_db():
    if "db" not in g:
        password = os.getenv("MYSQL_PASSWORD")
        if password is None:
            raise RuntimeError("Set the MYSQL_PASSWORD environment variable.")
        g.db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=password,
            database=os.getenv("MYSQL_DATABASE", "emp"),
        )
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def validate_csrf():
    submitted = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    if not expected or not secrets.compare_digest(submitted, expected):
        abort(400, description="Form expired. Reload the page and try again.")


def parse_salary(value, *, allow_zero):
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError):
        return None
    if not amount.is_finite() or amount < 0 or (not allow_zero and amount == 0):
        return None
    if amount > MAX_SALARY or amount.as_tuple().exponent < -2:
        return None
    return amount


def rollback_if_connected():
    connection = g.get("db")
    if connection is not None:
        connection.rollback()


@app.get("/")
def index():
    session.setdefault("csrf_token", secrets.token_hex(32))
    search = request.args.get("q", "").strip()
    try:
        with get_db().cursor() as cursor:
            if search:
                pattern = f"%{search}%"
                cursor.execute(
                    "SELECT id, name, position, salary FROM employees "
                    "WHERE id LIKE %s OR name LIKE %s OR position LIKE %s "
                    "ORDER BY id",
                    (pattern, pattern, pattern),
                )
            else:
                cursor.execute(
                    "SELECT id, name, position, salary FROM employees ORDER BY id"
                )
            employees = cursor.fetchall()
    except (mysql.connector.Error, RuntimeError) as err:
        employees = []
        flash(f"Could not load employees: {err}", "error")

    total_payroll = sum(
        (Decimal(str(employee[3])) for employee in employees), Decimal("0")
    )
    return render_template(
        "index.html",
        employees=employees,
        employee_count=len(employees),
        total_payroll=total_payroll,
        csrf_token=session["csrf_token"],
        search=search,
    )


@app.post("/employees")
def add_employee():
    validate_csrf()
    employee_id = request.form.get("employee_id", "").strip()
    name = request.form.get("name", "").strip()
    position = request.form.get("position", "").strip()
    salary = parse_salary(request.form.get("salary", ""), allow_zero=True)

    if not employee_id or len(employee_id) > 20:
        flash("Employee ID is required and must be 20 characters or fewer.", "warning")
    elif not name or len(name) > 100:
        flash("Name is required and must be 100 characters or fewer.", "warning")
    elif not position or len(position) > 100:
        flash("Position is required and must be 100 characters or fewer.", "warning")
    elif salary is None:
        flash("Enter a non-negative salary with up to two decimal places.", "warning")
    else:
        try:
            with get_db().cursor() as cursor:
                cursor.execute(
                    "INSERT INTO employees (id, name, position, salary) "
                    "VALUES (%s, %s, %s, %s)",
                    (employee_id, name, position, salary),
                )
            get_db().commit()
            flash("Employee added successfully.", "success")
        except (mysql.connector.Error, RuntimeError) as err:
            rollback_if_connected()
            flash(f"Could not add employee: {err}", "error")
    return redirect(url_for("index"))


@app.post("/employees/<employee_id>/remove")
def remove_employee(employee_id):
    validate_csrf()
    try:
        with get_db().cursor() as cursor:
            cursor.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
            removed = cursor.rowcount
        get_db().commit()
        flash(
            "Employee removed successfully." if removed else "Employee was not found.",
            "success" if removed else "warning",
        )
    except (mysql.connector.Error, RuntimeError) as err:
        rollback_if_connected()
        flash(f"Could not remove employee: {err}", "error")
    return redirect(url_for("index"))


@app.post("/employees/<employee_id>/promote")
def promote_employee(employee_id):
    validate_csrf()
    amount = parse_salary(request.form.get("amount", ""), allow_zero=False)
    if amount is None:
        flash("Enter a positive increase with up to two decimal places.", "warning")
        return redirect(url_for("index"))

    try:
        with get_db().cursor() as cursor:
            cursor.execute(
                "UPDATE employees SET salary=salary+%s WHERE id=%s",
                (amount, employee_id),
            )
            updated = cursor.rowcount
        get_db().commit()
        flash(
            "Employee salary increased successfully."
            if updated
            else "Employee was not found.",
            "success" if updated else "warning",
        )
    except (mysql.connector.Error, RuntimeError) as err:
        rollback_if_connected()
        flash(f"Could not promote employee: {err}", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", os.getenv("FLASK_PORT", "5000"))),
        debug=False,
    )
