import pymysql

from app import app
from flask import render_template, request, flash, redirect, session, url_for

@app.route("/staff_login", methods=['POST','GET'])
def delivery():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        category = request.form['category']
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if category == "Service_staff":
            cursor.execute("select * from employees where category = 'Service_staff' and employee_id = %s ", emp_id)
            if cursor.rowcount == 1:
                session['Service_staff'] = emp_id
                return redirect('/deliveries')
            else:
                flash("No Service staff found with the credentials given", "info")
                return render_template("staff/staff_login.html")
        elif category == "Kitchen_staff":
            cursor.execute("select * from employees where category = 'Kitchen_staff' and employee_id = %s ", emp_id)
            if cursor.rowcount == 1:
                session['Kitchen_staff'] = emp_id
                return redirect('/deliveries')
            else:
                flash("No Kitchen staff found with the credentials given", "info")
                return render_template("staff/staff_login.html")
        elif category == "Rider":
            cursor.execute("select * from employees where category = 'rider' and employee_id = %s ", emp_id)
            if cursor.rowcount == 1:
                session['rider'] = emp_id
                return redirect('/deliveries')
            else:
                flash("No rider found with the credentials given", "info")
                return render_template("staff/staff_login.html")
        else:
            flash("No employee found with the credentials given", "info")
            return render_template("staff/staff_login.html")
    else:
        return render_template("staff/staff_login.html")

