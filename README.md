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

## Deploy on Render

1. Push this repository to GitHub and create a Render **Web Service** connected
   to the repository.
2. Set the build command to `pip install -r requirements.txt`.
3. Set the start command to `gunicorn employee_management_flask:app --bind 0.0.0.0:$PORT`.
4. Add these environment variables in the Render service settings:
   - `MYSQL_HOST`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`
   - `FLASK_SECRET_KEY` (use a long, random value)
5. Ensure the hosted MySQL server permits connections from Render and that the
   `employees` table exists before using the app.

Render provides managed PostgreSQL, not a MySQL database service. This app uses
MySQL, so provide a separate hosted MySQL database. Switching to PostgreSQL
requires adapting the app's database driver and SQL connection code.