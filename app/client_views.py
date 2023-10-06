import pymysql

from app import app
from flask import render_template, request, flash,redirect, session, url_for
from uuid import uuid4
import pydataman as pd
app.secret_key = app.config['SECRET_KEY']

@app.route("/")
def index():
    return render_template("clients/index.html")

@app.route("/order_type")
def order_type():
    return render_template('clients/order_type.html')

@app.route("/inhouse", methods=['POST','GET'])
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

        cursor.execute("select * from device where uid = %s",duid)
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
                                       "table_id) values (%s,%s,%s,%s,%s)", (employee_id, fname, lname, duid, table_num))
                        cursor.execute("update device set status = 'assigned' where uid = %s", duid)
                        session['duid'] = duid
                        session['table'] = table_num
                        conn.commit()
                        return render_template("clients/inhouse.html")
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
# random string generator function
def ordercode():
    ident = uuid4().__str__()[:8]
    return f"{ident}"
@app.route("/addtocart", methods=['POST'])
def addtocart():
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
                                 'product_cost': row['price'], 'quantity': qtty, 'individual_price': 1 * row['price'],
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
        for key, value in session['cart_item'].items(): #takes and processes all the items in the cart item array
            # Each variable represents a particular session that is in the cart item
            ordercode =  session['cart_item'][key]['ordercode']
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
                        #individual_quantity = int(session['cart_item'][key]['quantity'])
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
def order( ):
    # if 'username' in session:
        if 'cart_item' in session:
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
                total =session['cart_item'][key]['total_price']

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
                    #     insert the records to the in-house orders tables
                    cursor = conn.cursor()
                    cursor.execute(
                        "insert into inhouse_orders(order_id,name,device_uid,table_number,cost,quantity,total) "
                        "values('{}','{}','{}','{}','{}','{}','{}')".format(
                            ordercode, name,device_no,table_no, cost, qtty, total))
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
    cursor.execute("select * from inhouse_orders where table_number = %s and device_uid = %s and status != %s",
                   (session['table'], session['duid'], "complete"))
    if cursor.rowcount > 0:
        rows = cursor.fetchall()
        # get total
        total_sum = 0
        for row in rows:
            total_sum = total_sum + row[7]
        return render_template('clients/my_orders.html', rows=rows, total_sum=total_sum)
    else:
        flash("You have no orders", "Warning")

# Route to logout
@app.route("/logout")
def logout():
    session.pop('cart_item', None)
    session.pop('all_total_quantity', None)
    session.pop('all_total_price', None)
    session.pop('duid', None)
    session.pop('table', None)