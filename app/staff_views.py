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
                return redirect('/inhouse_orders')
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

@app.route("/deliveries")
def deliveries():
    if "rider" in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from takeaway_orders where delivery_person = %s and status != %s ",
                       (session['rider'], "Complete"))
        if cursor.rowcount == 0:
            flash("You have no pending deliveries", "info")
            return render_template("staff/deliveries.html")
        else:
            rows = cursor.fetchall()
            total_sum = 0
            for row in rows:
                total_sum = total_sum + row [8]
            return render_template("staff/deliveries.html", rows=rows, total_sum=total_sum)
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")
@app.route("/inhouse_orders")
def food_orders():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from inhouse_orders group by order_id")
    rows = cursor.fetchall()
    return render_template("staff/kitchen/inhouse_orders.html", rows=rows)

@app.route("/takeaway_orders")
def takeaway_orders():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from takeaway_orders group by order_id")
    rows = cursor.fetchall()
    return render_template("staff/kitchen/takeaway_orders.html", rows=rows)

@app.route("/view/<order_id>")
def view(order_id):
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from inhouse_orders where order_id = %s", order_id)
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        return render_template("staff/kitchen/order_view.html", rows=rows)
    elif cursor.rowcount == 0:
        cursor.execute("select * from takeaway_orders where order_id = %s", order_id)
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("staff/kitchen/order_view.html", rows=rows)
        else:
            flash("No orders by that ID, try again", "warning")
            return render_template("staff/kitchen/order_view.html")