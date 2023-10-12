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
    if 'Kitchen_staff' in session:
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
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")


@app.route("/takeaway_orders")
def takeaway_orders():
    if 'Kitchen_staff' in session:
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
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")

@app.route("/view/<order_id>")
def view(order_id):
    if 'Kitchen_staff' or 'Service_staff' in session:
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
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")


@app.route("/assign_rider/<order_id>", methods=['POST', 'GET'])
def assign_rider(order_id):
    if 'Kitchen_staff' in session:
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
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")


@app.route("/done_prepping/<order_id>", methods=['POST', 'GET'])
def done_prepping(order_id):
    if 'Kitchen_staff' in session:
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
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")


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
    if 'Service_staff' or 'rider' in session:
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
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")
@app.route("/complete_orders")
def complete_orders():
    if 'Service_staff' in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from inhouse_orders where status = 'Complete' and served_by = %s", session['Service_staff'])
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("/staff/service/complete_orders.html", rows=rows)
        elif cursor.rowcount <= 0:
            flash("You do not have any complete orders", "info")
            return render_template("/staff/service/complete_orders.html")
    else:
        flash("Please login first", "info")
        return redirect("/staff_login")

@app.route("/logout_staff")
def logout_staff():
    if 'rider' in session:
        session.pop('rider', None)
    if 'Service_staff' in session:
        session.pop('Service_staff', None)
    if 'Kitchen_staff' in session:
        session.pop('Kitchen_staff', None)
    return redirect('/staff_login')
