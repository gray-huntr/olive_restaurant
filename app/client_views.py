import pymysql

from app import app
from flask import render_template, request, flash, redirect, session, url_for
from uuid import uuid4
import pydataman as pd
# mpesa integration
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth


app.secret_key = app.config['SECRET_KEY']


@app.route("/")
def index():
    return render_template("clients/index.html")


@app.route("/order_type")
def order_type():
    return render_template('clients/order_type.html')

@app.route("/reservations", methods=['POST','GET'])
def reservations():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        date = request.form['date']
        time = request.form['time']
        in_attendance = request.form['in_attendance']

        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("insert into reservations(in_attendance, name, number, date, time) values (%s,%s,%s,%s,%s)",
                       (in_attendance, name, number, date, time))
        conn.commit()
        flash("Your reservation has been received,", "success")
        return redirect("/reservations")
    else:
        return render_template("clients/reservations.html")





@app.route("/inhouse", methods=['POST', 'GET'])
def inhouse():
    if request.method == 'POST':
        duid = request.form['UID']
        table_num = request.form['tbl_number']
        employee_id = request.form['employee_id']

        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()

        cursor.execute("select * from device where uid = %s", duid)
        if cursor.rowcount == 1:
            cursor.execute("select * from tables where table_id = %s", table_num)
            if cursor.rowcount == 1:
                cursor.execute("select * from employees where employee_id = %s", employee_id)
                if cursor.rowcount == 1:
                    rows = cursor.fetchall()
                    for row in rows:
                        fname = row[1]
                        lname = row[2]
                        cursor.execute("insert into table_assignments(assignee_id, first_name, last_name, device_uid, "
                                       "table_id) values (%s,%s,%s,%s,%s)",
                                       (employee_id, fname, lname, duid, table_num))
                        cursor.execute("update device set status = 'assigned' where uid = %s", duid)
                        session['duid'] = duid
                        session['table'] = table_num
                        conn.commit()
                        return redirect("/food_menu")
                else:
                    flash("Incorrect UID, table number or author code", category="primary")
                    return redirect('/inhouse')
            else:
                flash("Incorrect UID, table number or author code", category="primary")
                return redirect('/inhouse')
        else:
            flash("Incorrect UID, table number or author code", category="primary")
            return redirect('/inhouse')
    else:
        return render_template('clients/inhouse.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        password = request.form['password']
        rep_pass = request.form['repeat_pass']
        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        # Check first whether there is an already existing account
        cursor.execute("select * from clients where email = %s ", email)
        if cursor.rowcount > 0:
            flash("Username already exists", "warning")
            return render_template('clients/sign_up.html')
        else:
            # if there is no existing account, check whether the two passwords match
            if password == rep_pass:
                #     insert the records to the users tables
                cursor.execute(
                    "insert into clients(first_name,last_name,email,number,location,password) values (%s,%s,%s,%s,%s,%s)",
                    (fname, lname, email, phone, location, password))
                # save records
                conn.commit()
                # redirect them to login page
                return render_template('clients/login.html', )
                # if passwords do not match display the following message
            elif password != rep_pass:
                flash("Passwords do not match", "danger")
                return render_template('clients/sign_up.html')
            else:
                flash("Error occurred please try again", "info")
                return render_template('clients/sign_up.html')
    else:
        return render_template('clients/sign_up.html')


@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        #  connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        # pick the record from the clients table
        cursor = conn.cursor()
        cursor.execute("select * from clients where email =%s and password=%s", (email, password))
        # if cursor.rowcount == 1:
        if cursor.rowcount == 1:
            session['email'] = email
            return redirect('/food_menu')
        elif cursor.rowcount == 0:
            flash("User does not exist or incorrect password", "warning")
            return render_template('clients/login.html')

        # elif cursor.rowcount == 0:
        #     cursor.execute("select * from admins where email =%s and password=%s", (email, password))
        #     if cursor.rowcount == 1:
        #         return render_template('admin.html', msg="login successful")
        #     elif cursor.rowcount == 0:
        #         flash("User does not exist or incorrect password", "warning")
        #         return render_template('clients/login.html')
    else:
        return render_template('clients/login.html')


@app.route("/food_menu")
def food_menu():
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from menu where category = 'Food'")
    if cursor.rowcount > 1:
        rows = cursor.fetchall()
        return render_template('clients/food_menu.html', rows=rows)
    else:
        flash("Out of stock please wait for a restock and try again later")
        return redirect('/order_type')


@app.route("/drink_menu")
def drink_menu():
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from menu where category = 'Drinks'")
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        return render_template('clients/drink_menu.html', rows=rows)
    else:
        flash("Out of stock please wait for a restock and try again later")
        return redirect('/order_type')


@app.route("/appetizer_menu")
def appetizer_menu():
    #  connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select * from menu where category = 'Appetizer'")
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        return render_template('clients/appetizer_menu.html', rows=rows)
    else:
        flash("Out of stock please wait for a restock and try again later")
        return redirect('/order_type')


# random string generator function
def ordercode():
    ident = uuid4().__str__()[:8]
    return f"{ident}"


@app.route("/addtocart/<category>", methods=['POST'])
def addtocart(category):
    if category == "Food":
        id = request.form['id']
        qtty = int(request.form['quantity'])
        # create a unique code from the random string generator route
        code = ordercode()
        # validate the received values
        if id and request.method == 'POST':
            conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                   password=app.config["DB_PASSWORD"],
                                   database=app.config["DB_NAME"])
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM menu WHERE id= %s", id)
            row = cursor.fetchone()

            # An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together
            # am item array is created from the data above fetched from the database
            # it is under the random string generated with the route above
            itemArray = {str(code): {'product_name': row['name'], 'product_id': row['id'],
                                     'product_cost': row['price'], 'quantity': qtty,
                                     'individual_price': 1 * row['price'],
                                     'total_price': int(qtty) * row['price'], 'ordercode': code}}
            # print the item array on the terminal, can be removed....
            # print((itemArray))

            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            # if there is an item already
            if 'cart_item' in session:
                # a new product added in the cart to Merge the previous to have a new cart item with two products
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
                #  for each item in the array
                for key, value in session['cart_item'].items():
                    individual_quantity = 1
                    individual_total_price = session['cart_item'][key]['total_price']
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_total_price


            else:
                # if the cart is empty you add the whole item array and create a session
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + 1
                # get total price by multiplying the cost and the quantity
                all_total_price = all_total_price + int(qtty) * row['price']

            # add total quantity and total price to a session
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            flash('Order added to cart successfully', 'success')
            return redirect(url_for('.food_menu'))
        else:
            return 'Error while adding item to cart'
    elif category == "Drink":
        id = request.form['id']
        qtty = int(request.form['quantity'])
        soda = request.form['soda']
        price = int(request.form['size'])

        if price == 60:
            size = "300 ML"
        else:
            size = "500 ML"
        # create a unique code from the random string generator route
        code = ordercode()
        # validate the received values
        if id and request.method == 'POST':
            conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                   password=app.config["DB_PASSWORD"],
                                   database=app.config["DB_NAME"])
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM menu WHERE id= %s", id)
            row = cursor.fetchone()

            # An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together
            # am item array is created from the data above fetched from the database
            # it is under the random string generated with the route above
            itemArray = {str(code): {'product_name': soda + f" ({size})", 'product_id': row['id'],
                                     'product_cost': price, 'quantity': qtty,
                                     'individual_price': 1 * price,
                                     'total_price': qtty * price, 'ordercode': code}}
            # print the item array on the terminal, can be removed....
            # print((itemArray))

            all_total_price = 0
            all_total_quantity = 0
            session.modified = True
            # if there is an item already
            if 'cart_item' in session:
                # a new product added in the cart to Merge the previous to have a new cart item with two products
                session['cart_item'] = array_merge(session['cart_item'], itemArray)
                #  for each item in the array
                for key, value in session['cart_item'].items():
                    individual_quantity = 1
                    individual_total_price = session['cart_item'][key]['total_price']
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_total_price


            else:
                # if the cart is empty you add the whole item array and create a session
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + 1
                # get total price by multiplying the cost and the quantity
                all_total_price = all_total_price + int(qtty) * int(price)

            # add total quantity and total price to a session
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

            flash('Order added to cart successfully', 'success')
            return redirect(url_for('.drink_menu'))
        else:
            flash('Error while adding item to cart', 'warning')
            return redirect(url_for('.drink_menu'))


@app.route('/cart')
def cart():
    return render_template('clients/cart.html')


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    # takes the new product add to the existing and merge to have one array with two products
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False


# Route to empty the cart
@app.route('/empty')
def empty_cart():
    try:
        for key, value in session['cart_item'].items():  # takes and processes all the items in the cart item array
            # Each variable represents a particular session that is in the cart item
            ordercode = session['cart_item'][key]['ordercode']
            # id = session['cart_item'][key]['product_id']
            # quantity =  session['cart_item'][key]['quantity']
            # for item in session['cart_item'].items():
            # for each item in the cart item array check whether the value at index 0 is equal to the order code
            # if item[0] == ordercode:
            #     conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
            #                            password=app.config["DB_PASSWORD"],
            #                            database=app.config["DB_NAME"])
            #     cursor = conn.cursor()
            # cursor.execute("select * from menu where product_id = '{}'".format(id))
            # # first checks if the id matches with any data in the menu table, if it matches,it will take the below route, if not.....else route
            # if cursor.rowcount == 1:
            #     rows = cursor.fetchall()
            #     # if the cart is emptied, the quantity of each item in the item array is reverted back to its original number before it was added to cart
            #     for row in rows:
            #         stock = row[5]
            #         new_stock = stock + int(quantity)
            #         cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
            #         conn.commit()
            # else:
            #     cursor.execute("select * from tech where product_id = '{}'".format(id))
            #     rows = cursor.fetchall()
            #     for row in rows:
            #         stock = row[4]
            #         new_stock = stock + int(quantity)
            #         cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
            #         conn.commit()

        # after all the emptying is done, the function clears the below sessions leaving the cart empty
        if 'cart_item' in session or 'all_total_quantity' in session or 'all_total_price' in session:
            session.pop('cart_item', None)
            session.pop('all_total_quantity', None)
            session.pop('all_total_price', None)
            return redirect(url_for('.cart'))
        else:
            return redirect(url_for('.cart'))

    except Exception as e:
        print(e)


@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == code:
                # conn = pymysql.connect(host="localhost", user="root", password="", database="game_store")
                # cursor = conn.cursor()
                # cursor.execute("select * from games where product_id = '{}'".format(id))
                # if cursor.rowcount == 1:
                #     rows = cursor.fetchall()
                #     for row in rows:
                #         stock = row[5]
                #         new_stock = stock + int(quantity)
                #         cursor.execute("update games set quantity = %s where product_id = %s", (new_stock, id))
                #         conn.commit()
                # else:
                #     cursor.execute("select * from tech where product_id = '{}'".format(id))
                #     rows = cursor.fetchall()
                #     for row in rows:
                #         stock = row[4]
                #         new_stock = stock + int(quantity)
                #         cursor.execute("update tech set quantity = %s where product_id = %s", (new_stock, id))
                #         conn.commit()

                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        # individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_total_price = session['cart_item'][key]['total_price']
                        all_total_quantity = all_total_quantity + 1
                        all_total_price = all_total_price + individual_total_price
                break

        if all_total_quantity == 0:
            session.pop('cart_item', None)
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect(url_for('.cart'))

    except Exception as e:
        print(e)


# Create a unique order code
def receiptcode():
    # i = 1000
    # pd.save('code', i)
    var = pd.read('code')
    while var < 10000000:
        new = var + 1
        pd.save('code', new)
        var2 = "J" + str(pd.read('code')) + "V"
        return f"{var2}"
    else:
        flash("Order codes deplited")


# Place inhouse orders in database
@app.route('/order', methods=['POST', 'GET'])
def order():
    # if 'username' in session:
    if 'cart_item' in session:
        if 'duid' and 'table' in session:
            all_total_price = 0
            all_total_quantity = 0
            ordercode = receiptcode()
            for key, value in session['cart_item'].items():
                individual_quantity = 1
                individual_total_price = session['cart_item'][key]['total_price']
                name = session['cart_item'][key]['product_name']
                device_no = session['duid']
                table_no = session['table']
                cost = session['cart_item'][key]['product_cost']
                qtty = session['cart_item'][key]['quantity']
                total = session['cart_item'][key]['total_price']

                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_total_price

                # session
                if not device_no or not table_no:
                    return redirect('/order_type')
                elif not individual_total_price or not individual_quantity or not name or not all_total_price or not all_total_quantity:
                    return redirect('/cart')
                else:
                    # we first connect to local host and game_store database
                    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                           password=app.config["DB_PASSWORD"],
                                           database=app.config["DB_NAME"])
                    cursor = conn.cursor()
                    # insert the records to the in-house orders tables
                    cursor.execute(
                        "insert into inhouse_orders(order_id,name,device_uid,table_number,cost,quantity,total) "
                        "values('{}','{}','{}','{}','{}','{}','{}')".format(
                            ordercode, name, device_no, table_no, cost, qtty, total))
                    cursor.execute("update tables set status = 'in use' where table_id = %s", session['table'])
                    conn.commit()
            session.pop('cart_item', None)
            session.pop('all_total_quantity', None)
            session.pop('all_total_price', None)
            return render_template('clients/cart.html', msg='Your order(s) have been placed successfully')
        elif 'email' in session:
            all_total_price = 0
            all_total_quantity = 0
            ordercode = receiptcode()
            for key, value in session['cart_item'].items():
                individual_quantity = 1
                individual_total_price = session['cart_item'][key]['total_price']
                name = session['cart_item'][key]['product_name']
                cost = session['cart_item'][key]['product_cost']
                qtty = session['cart_item'][key]['quantity']
                total = session['cart_item'][key]['total_price']

                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_total_price

                # session
                if not session['email']:
                    return redirect('/order_type')
                elif not individual_total_price or not individual_quantity or not name or not all_total_price or not all_total_quantity:
                    return redirect('/cart')
                else:
                    # we first connect to local host and game_store database
                    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                           password=app.config["DB_PASSWORD"],
                                           database=app.config["DB_NAME"])
                    cursor = conn.cursor()
                    # get the data that is related to the currently logged in user
                    cursor.execute("SELECT * FROM clients WHERE email= %s", session['email'])
                    if cursor.rowcount == 1:
                        rows = cursor.fetchall()
                        for row in rows:
                            username = row[0]
                            number = row[3]
                            location = row[4]
                            #     insert the records to the takeaway orders tables
                            cursor.execute(
                                "insert into takeaway_orders(order_id,name,email,ordered_by,number,delivery_location,cost,quantity,total)"
                                "values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                                    ordercode, name,session['email'], username, number, location, cost, qtty, total))
                            conn.commit()
            session.pop('cart_item', None)
            session.pop('all_total_quantity', None)
            session.pop('all_total_price', None)
            return render_template('clients/cart.html', msg='Your order(s) have been placed successfully')


# else:
#     session['page'] = "checkout"
#     return redirect ('/users_login')

# route for clients to view their orders
@app.route("/my_orders")
def my_orders():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if 'email' in session:
        cursor.execute("select * from takeaway_orders where email = %s",
                       (session['email']))
    else:
        cursor.execute("select * from inhouse_orders where table_number = %s and device_uid = %s and status != %s",
                       (session['table'], session['duid'], "complete"))
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        # get total
        total_sum = 0
        for row in rows:
            total_sum = total_sum + row[8]
        return render_template('clients/my_orders.html', rows=rows, total_sum=total_sum)
    else:
        flash("You have no pending orders", 'Warning')
        return render_template('clients/my_orders.html')

@app.route('/mpesa_payment', methods = ['POST','GET'])
def mpesa_payment():
    # conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
    #                        password=app.config["DB_PASSWORD"],
    #                        database=app.config["DB_NAME"])
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM clients where username = %s", (session['username']))
    # # AFter executing the query above, get all rows
    # number = cursor.fetchall()
    # session['request'] = 'accept'

    if request.method == 'POST':
        phone = str(int(request.form['phone']))
        phone = str("254") + phone
        # account = request.form['account']
        # amount = str(request.form['amount'])

        #GENERATING THE ACCESS TOKEN
        consumer_key = "0aDsNA5rkQiAFJY594KxPtDkAfyZp51s"
        consumer_secret = "b96yLzkGAP5Lt44j"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')


        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1", #use 1 when testing
            "PartyA": phone, #phone number that is paying
            "PartyB": "174379", #paybill number
            "PhoneNumber": phone, #phone number that is paying
            "CallBackURL": "https://0b97-196-202-162-46.ngrok.io/callback" ,
            "AccountReference": "Olive restaurant",
            "TransactionDesc": "account"
        }

        # POPULATING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(phone)
        print (response.text)
        session.pop('request', None)
        if 'rider' in session:
            flash("Tell client to complete order on phone", "info")
            return redirect('/deliveries')
        else:
            flash("Complete payment on phone", "info")
            return redirect('/my_orders')
    else:
        return redirect('/my_orders')

# @app.route("/callback")
# def callback():
#     subprocess.call("php app/call.php")
    # proc = subprocess.Popen("php app/call.php", shell=True, stdout=subprocess.PIPE)
    # script_response = proc.stdout.read()
    # print(script_response)


# Route to log out
@app.route("/logout")
def logout():
    session.pop('cart_item', None)
    session.pop('all_total_quantity', None)
    session.pop('all_total_price', None)
    session.pop('duid', None)
    session.pop('table', None)
    session.pop('email', None)
    return redirect('/')
