# HR Analytics to Track Employee Performance

Employee management application with a Flask dashboard backed by MySQL.

## Setup

1. Install Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Set the MySQL password in PowerShell. Optionally set a different database user:

   ```powershell
   $env:MYSQL_PASSWORD = "your_mysql_password"
   $env:MYSQL_USER = "root"
   ```

3. Create the database and employee table:

   ```powershell
   python .\connection1.py
   ```

4. Start the web application:

   ```powershell
   python .\employee_management_flask.py
   ```

5. Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

The app also accepts `MYSQL_HOST`, `MYSQL_DATABASE`, `FLASK_HOST`, `FLASK_PORT`,
and `FLASK_SECRET_KEY` environment variables. Do not commit credentials or `.env`
files.