from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="$DB_HOST",
    user="$DB_USER",
    password="$DB_PASSWORD",
    database="$DB_NAME"
)

cursor = db.cursor()

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    employee_id = request.form['employee_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    department = request.form['department']
    email = request.form['email']
    phone = request.form['phone']
    date_of_joining = request.form['date_of_joining']

    # Insert form data into the database
    sql = "INSERT INTO employees (employee_id, first_name, last_name, department, email, phone, date_of_joining) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (employee_id, first_name, last_name, department, email, phone, date_of_joining)
    cursor.execute(sql, val)
    db.commit()

    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
