from app import app
from flask import render_template, request, flash, redirect,session
import pymysql
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])


@app.route("/admin_login", methods=['POST', 'GET'])
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
            return redirect('/menu_upload')
        elif cursor.rowcount == 0:
            flash("User does not exist or incorrect password", "warning")
            return render_template('admin/admin_login.html')
    return render_template('admin/admin_login.html')


@app.route("/admin_signup", methods=['POST', 'GET'])
def admin_signup():
    if 'admin' in session:
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
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")



@app.route("/new_employee", methods=['POST', 'GET'])
def new_employee():
    if 'admin' in session:
        if request.method == 'POST':
            with open("data/employee_id", "r") as file:
                old_id = int(file.read())
                employee_id = "W00" + str(old_id)
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
            cursor.execute("select * from employees where email = %s and employee_id = %s ", (email, employee_id))
            if cursor.rowcount > 0:
                flash("Email or employee id already exists, try another one", "warning")
                return render_template('admin/new_employee.html')
            elif cursor.rowcount == 0:
                # if there is no existing account, proceed
                #     insert the records to the employees tables
                cursor.execute(
                    "insert into employees(employee_id,first_name,last_name,number,email,category) values (%s,%s,%s,%s,%s,%s)",
                    (employee_id, fname, lname, phone, email, category))
                # save records
                conn.commit()
                old_id += 1
                # save it to file
                with open("data/employee_id", "w") as file:
                    file.write(str(old_id))
                flash("Employee signed up successfully", "success")
                return render_template('admin/new_employee.html', )
            else:
                flash("Error occurred please try again", "info")
                return render_template('admin/new_employee.html')
        else:
            return render_template('admin/new_employee.html')
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")


@app.route("/employee_records", methods=['POST', 'GET'])
def employee_records():
    if 'admin' in session:
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
                           "where employee_id = %s ", (fname, lname, number, email, category, id))
            conn.commit()
            flash("Records updated successfully", "success")
            return redirect("/employee_records")
        else:
            cursor.execute("select * from employees")
            rows = cursor.fetchall()
            return render_template("admin/employee_records.html", rows=rows)
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")

@app.route("/employee_search", methods=['POST','GET'])
def employee_search():
    if 'admin' in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            search_term = request.form['search_term']

            cursor.execute("select * from employees where first_name like %s or last_name like %s or employee_id = %s",
                           ('%' + search_term + '%', '%' + search_term + '%', search_term))
            if cursor.rowcount > 0:
                rows = cursor.fetchall()
                return render_template("admin/employee_records.html", rows=rows)
            elif cursor.rowcount == 0:
                flash("Record does not exist", "danger")
                return redirect("/employee_records")
        else:
            return redirect("/employee_records")
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")


@app.route("/menu_upload", methods=['POST', 'GET'])
def menu_upload():
    if 'admin' in session:
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part', "warning")
                return redirect("/menu_upload")
            file = request.files['file']
            name = request.form['name']
            price = request.form['price']
            category = request.form['category']
            description = request.form['description']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file', 'warning')
                return redirect('/menu_upload')
            # If all checks are passed, the app proceeds to submit the file

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                sql = ("insert into menu(name,picture,description,price,category) "
                       "values(%s,%s,%s,%s,%s)")
                try:

                    # send to database
                    cursor.execute(sql, (name, filename, description, price, category))
                    # Save to database
                    conn.commit()
                    flash("Uploaded Successfully", "success")
                    return redirect('/menu_upload')
                    # if error occurs, display error message
                except:
                    flash("Upload Failed", "danger")
                    return redirect('/menu_upload')
            # If file is not on allowed list, display error message
            else:
                flash("Uploaded File Not Allowed", "warning")
                return redirect('/menu_upload')
        else:
            cursor.execute("select * from menu")
            rows = cursor.fetchall()
            return render_template('admin/menu_upload.html', rows=rows)
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")

@app.route("/menu/<action>", methods=['POST','GET'])
def menu(action):
    if 'admin' in session:
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if action == 'update':
            if request.method == 'POST':
                id = request.form['id']
                name = request.form['name']
                description = request.form['description']
                price = request.form['price']
                category = request.form['category']

                cursor.execute("update menu set name = %s, description = %s, price = %s, category = %s "
                               "where id = %s", (name,description, price, category, id))
                conn.commit()
                flash("Menu updated successfully", "success")
                return redirect("/menu_upload")
            else:
                return redirect("/menu_upload")
        elif action == "search":
            if request.method == 'POST':
                menuitem = request.form['menuitem']

                cursor.execute("select * from menu where name like %s",('%' + menuitem + '%'))
                if cursor.rowcount > 0:
                    rows = cursor.fetchall()
                    return render_template('admin/menu_upload.html', rows=rows)
                elif cursor.rowcount == 0:
                    flash("There are no menu items with the given name", "info")
                    return redirect("/menu_upload")
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")




@app.route("/adm_inhouse_orders", methods=['POST','GET'])
def adm_inhouse_orders():
    if 'admin' in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            id = request.form['id']

            cursor.execute("select * from inhouse_orders where order_id = %s group by order_id",
                           id)
            if cursor.rowcount > 0:
                rows = cursor.fetchall()
                return render_template("admin/adm_inhouse_orders.html", rows=rows)
            elif cursor.rowcount == 0:
                flash(f"There is no order under the id {id}", "warning")
                return redirect("/adm_inhouse_orders")
        else:
            cursor.execute("select * from inhouse_orders group by order_id")
            rows = cursor.fetchall()
            return render_template("admin/adm_inhouse_orders.html", rows=rows)
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")


@app.route("/adm_takeaway_orders", methods=['POST','GET'])
def adm_takeaway_orders():
    if 'admin' in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            id = request.form['id']

            cursor.execute("select * from takeaway_orders where order_id = %s group by order_id",
                           id)
            if cursor.rowcount > 0:
                rows = cursor.fetchall()
                return render_template("admin/adm_takeaway_orders.html", rows=rows)
            elif cursor.rowcount == 0:
                flash(f"There is no order under the id {id}", "warning")
                return redirect("/adm_takeaway_orders")
        else:
            cursor.execute("select * from takeaway_orders group by order_id")
            rows = cursor.fetchall()
            return render_template("admin/adm_takeaway_orders.html", rows=rows)
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")


@app.route("/appliances", methods=['POST','GET'])
def appliances():
    if 'admin' in session:
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if request.method == 'POST':
            id = request.form['id']
            category = request.form['category']

            if category == 'table':
                cursor.execute("select * from tables where table_id = %s", id)
                if cursor. rowcount > 0:
                    flash("The id you have entered already exists", "warning")
                    return redirect("/appliances")
                else:
                    cursor.execute("insert into tables(table_id) values (%s)",id)
                    conn.commit()
                    flash("Device added succesfully", "success")
                    return redirect("/appliances")
            elif category == 'device':
                cursor.execute("select * from device where uid = %s", id)
                if cursor.rowcount > 0:
                    flash("The id you have entered already exists", "warning")
                    return redirect("/appliances")
                else:
                    cursor.execute("insert into device(uid) values (%s)", id)
                    conn.commit()
                    flash("Device added succesfully", "success")
                    return redirect("/appliances")
            else:
                flash("Select the correct category", "danger")
                return redirect("/appliances")
        else:
            cursor.execute("select * from tables")
            tables = cursor.fetchall()
            cursor.execute("select * from device")
            tablets = cursor.fetchall()
            return render_template("admin/appliances.html", tables=tables, tablets=tablets)
    else:
        flash("Please log in first", "info")
        return redirect("/admin_login")


@app.route("/logout_admin")
def logout_admin():
    session.pop('admin', None)
    return redirect('/admin_login')