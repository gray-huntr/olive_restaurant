import pymysql

from app import app
from flask import render_template, request, flash, redirect, session, url_for

# Route for staff login
@app.route("/staff_login", methods=['POST', 'GET'])
def staff_login():
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
                rows = cursor.fetchall()
                for row in rows:
                    session['Service_staff'] = row[0] + row[1]
                    return redirect('/service')
            else:
                flash("No Service staff found with the credentials given", "info")
                return render_template("staff/staff_login.html")
        elif category == "Kitchen_staff":
            cursor.execute("select * from employees where category = 'Kitchen_staff' and employee_id = %s ", emp_id)
            if cursor.rowcount == 1:
                rows = cursor.fetchall()
                for row in rows:
                    session['Kitchen_staff'] = row[0] + row[1]
                    return redirect('/inhouse_orders')
            else:
                flash("No Kitchen staff found with the credentials given", "info")
                return render_template("staff/staff_login.html")
        elif category == "Rider":
            cursor.execute("select * from employees where category = 'rider' and employee_id = %s ", emp_id)
            if cursor.rowcount == 1:
                rows = cursor.fetchall()
                for row in rows:
                    session['rider'] = row[0] + row[1]
                    return redirect('/deliveries')
            else:
                flash("No rider found with the credentials given", "info")
                return render_template("staff/staff_login.html")
        else:
            flash("No employee found with the credentials given", "info")
            return render_template("staff/staff_login.html")
    else:
        return render_template("staff/staff_login.html")

# Route for delivery person
@app.route("/deliveries")
def deliveries():
    if "rider" in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from takeaway_orders where delivery_person = %s and status != %s group by order_id",
                       (session['rider'], "Complete"))
        if cursor.rowcount == 0:
            flash("You have no pending deliveries", "info")
            return render_template("staff/rider/deliveries.html")
        else:
            rows = cursor.fetchall()
            cursor.execute("select sum(total) from takeaway_orders")
            total_sum = cursor.fetchone()[0]
            # for row in rows:
            #     total_sum = total_sum + row[8]
            return render_template("staff/rider/deliveries.html", rows=rows, total_sum=total_sum)
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")

# Routes for the kitchen staff

@app.route("/inhouse_orders")
def food_orders():
    if 'order_id' in session:
        session.pop('order_id', None)
        return redirect("/inhouse_orders")
    else:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from inhouse_orders where status !='Complete' group by order_id")
        rows = cursor.fetchall()
        return render_template("staff/kitchen/inhouse_orders.html", rows=rows)


@app.route("/takeaway_orders")
def takeaway_orders():
    if "order_id" in session:
        session.pop('order_id', None)
        return redirect("/takeaway_orders")
    else:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from takeaway_orders where status != 'Complete' group by order_id")
        rows = cursor.fetchall()
        cursor.execute("select * from employees where category = 'Rider'")
        rider = cursor.fetchall()
        return render_template("staff/kitchen/takeaway_orders.html", rows=rows, rider=rider)


@app.route("/view/<order_id>")
def view(order_id):
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from inhouse_orders where order_id = %s", order_id)
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        total_sum = 0
        for row in rows:
            session['order_id'] = row[1]
            total_sum = total_sum + row[8]
        return render_template("staff/kitchen/order_view.html", rows=rows, total_sum=total_sum)
    elif cursor.rowcount == 0:
        cursor.execute("select * from takeaway_orders where order_id = %s", order_id)
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            for row in rows:
                session['order_id'] = row[1]
            return render_template("staff/kitchen/order_view.html", rows=rows)
        else:
            flash("No orders by that ID, try again", "warning")
            return render_template("staff/kitchen/order_view.html")


@app.route("/assign_rider/<order_id>", methods=['POST', 'GET'])
def assign_rider(order_id):
    if request.method == 'POST':
        name = request.form['name']
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if name == "":
            flash("You have not selected a rider try again", "danger")
            return redirect("/takeaway_orders")
        else:
            cursor.execute("update takeaway_orders set Delivery_person = %s where order_id = %s ", (name, order_id))
            conn.commit()
            flash("Rider has been assigned successfully", "info")
            return redirect("/takeaway_orders")


@app.route("/done_prepping/<order_id>", methods=['POST', 'GET'])
def done_prepping(order_id):
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from inhouse_orders where order_id = %s", order_id)
    if cursor.rowcount > 0:
        cursor.execute("update inhouse_orders set status = %s where order_id = %s ", ("On its way", order_id))
        conn.commit()
        flash("Status has been changed successfully", "info")
        return redirect(f"/view/{order_id}")
    elif cursor.rowcount == 0:
        cursor.execute("update takeaway_orders set status = %s where order_id = %s ", ("On its way", order_id))
        conn.commit()
        flash("Status has been changed successfully", "info")
        return redirect(f"/view/{order_id}")


# Routes for the service staff
@app.route("/service")
def service():
    if 'Service_staff' in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from inhouse_orders group by order_id")
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("staff/service/service_portal.html", rows=rows)
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")

@app.route("/complete/<order_id>")
def complete(order_id):
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from inhouse_orders where order_id = %s", order_id)
    if cursor.rowcount > 0:
        cursor.execute("update inhouse_orders set status = %s, served_by = %s  where order_id = %s ",
                       ("Complete", session['Service_staff'], order_id))
        conn.commit()
        flash("Order has been completed successfully", "info")
        return redirect("/service")
    elif cursor.rowcount == 0:
        cursor.execute("update takeaway_orders set status = %s where order_id = %s ", ("Complete", order_id))
        conn.commit()
        flash("Order has been completed successfully", "info")
        return redirect("/deliveries")
@app.route("/complete_orders")
def complete_orders():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from inhouse_orders where status = 'Complete'")
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        return render_template("/staff/service/complete_orders.html", rows=rows)
    elif cursor.rowcount <= 0:
        flash("You do not have any complete orders", "info")
        return render_template("/staff/service/complete_orders.html")

@app.route("/logout_staff")
def logout_staff():
    if 'rider' in session:
        session.pop('rider', None)
    if 'Service_staff' in session:
        session.pop('Service_staff', None)
    if 'Kitchen_staff' in session:
        session.pop('Kitchen_staff', None)
    return redirect('/staff_login')

# Routes for the admins

@app.route("/admin_login", methods=['POST','GET'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        # pick the record from the clients table
        cursor = conn.cursor()
        cursor.execute("select * from admins where email =%s and password=%s", (email, password))
        # if cursor.rowcount == 1:
        if cursor.rowcount == 1:
            session['admin'] = email
            return redirect('/admin_portal')
        elif cursor.rowcount == 0:
            flash("User does not exist or incorrect password", "warning")
            return render_template('admin/admin_login.html')
    return render_template('admin/admin_login.html')
@app.route("/admin_signup", methods=['POST','GET'])
def admin_signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        rep_pass = request.form['repeat_pass']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        # Check first whether there is an already existing account
        cursor.execute("select * from admins where email = %s ", email)
        if cursor.rowcount > 0:
            flash("Email already exists", "warning")
            return render_template('admin/admin_signup.html')
        else:
            # if there is no existing account, check whether the two passwords match
            if password == rep_pass:
                #     insert the records to the users tables
                cursor.execute(
                    "insert into admins(first_name,last_name,email,number,password) values (%s,%s,%s,%s,%s)",
                    (fname, lname, email, phone, password))
                # save records
                conn.commit()
                flash("Admin signed up successfully", "success")
                return render_template('admin/admin_signup.html', )
                # if passwords do not match display the following message
            elif password != rep_pass:
                flash("Passwords do not match", "danger")
                return render_template('admin/admin_signup.html')
            else:
                flash("Error occurred please try again", "info")
                return render_template('admin/admin_signup.html')
    else:
        return render_template('admin/admin_signup.html')

@app.route("/admin_portal")
def admin_portal():
    return render_template("admin/admin_portal.html")

@app.route("/new_employee", methods=['POST','GET'])
def new_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        category = request.form['category']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        # Check first whether there is an already existing account
        cursor.execute("select * from employees where email = %s and employee_id = %s ", (email,employee_id))
        if cursor.rowcount > 0:
            flash("Email or employee id already exists, try another one", "warning")
            return render_template('admin/new_employee.html')
        elif cursor.rowcount == 0:
            # if there is no existing account, proceed
                #     insert the records to the employees tables
                cursor.execute(
                    "insert into employees(employee_id,first_name,last_name,number,email,category) values (%s,%s,%s,%s,%s,%s)",
                    (employee_id,fname, lname, phone, email, category ))
                # save records
                conn.commit()
                flash("Employee signed up successfully", "success")
                return render_template('admin/new_employee.html', )
        else:
            flash("Error occurred please try again", "info")
            return render_template('admin/new_employee.html')
    else:
        return render_template('admin/new_employee.html')

@app.route("/employee_records", methods=['POST','GET'])
def employee_records():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        number = request.form['number']
        email = request.form['email']
        category = request.form['category']
        cursor.execute("update employees set first_name = %s, last_name = %s, number = %s, email = %s, category=%s "
                       "where employee_id = %s ", (fname,lname,number,email,category,id))
        conn.commit()
        flash("Records updated successfully", "success")
        return redirect("/employee_records")
    else:
        cursor.execute("select * from employees")
        rows = cursor.fetchall()
        return render_template("admin/employee_records.html", rows=rows)