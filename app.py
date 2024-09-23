# Author: Rasim Berke Turan, Istanbul Technical University
# Date: 12/21/2023
# Description: This is a Flask App that uses SQLite3 to

import sqlite3
from flask import Flask, render_template, request, redirect, Blueprint, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 

app = Flask(__name__)

# Add this function at the beginning of your Flask application file
def is_type_exist(type_name):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM restaurant_type WHERE type=?", (type_name,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False
    
def get_user_by_id(user_id):
    # Function to retrieve user details by ID from the database
    # Implement this function based on your database structure
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()
        return user    
def get_restaurant_by_id(restaurant_id):
    # Function to retrieve user details by ID from the database
    # Implement this function based on your database structure
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM restaurants WHERE id=?", (restaurant_id,))
        restaurant = cur.fetchone()
        return restaurant 
    
def is_user_id_exist(user_id):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False

def is_email_exist(email):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT email FROM users WHERE email=?", (email,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False

def get_menus_for_page(page, per_page, sort_by, order):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'title', 'price', 'restaurant_id', 'food_type_id']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    # Calculate the offset based on the page number and number of menus per page
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT menus.id as id, menus.title as title, menus.price as price, menus.description as description, restaurants.name as restaurant_name, restaurant_type.type as food_type FROM menus left join restaurants on restaurants.id = menus.restaurant_id left join restaurant_type on restaurant_type.id = menus.food_type_id ORDER BY {sort_by} {order} LIMIT ? OFFSET ?", (per_page, offset))
        menus = cur.fetchall()

    return menus

def get_total_menus():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM menus")
        total_menus = cur.fetchone()[0]

    return total_menus

def is_user_exist(user_name):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT user_name FROM users WHERE user_name=?", (user_name,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False
    
def get_all_restaurant_types():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, type FROM restaurant_type")
            restaurant_types = [dict(row) for row in cur.fetchall()]
            return restaurant_types
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []
    
def get_all_restaurants(sort_by='id', order='asc'):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print(order)
        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT * FROM restaurants ORDER BY {sort_by} {order}")
        restaurants = cur.fetchall()

    return restaurants


def get_all_menus(n):
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, title FROM menus  LIMIT 20 OFFSET (?-1)*20",(n))
            menus = [dict(row) for row in cur.fetchall()]
            return menus
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []
        
def get_all_menus():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, title FROM menus")
            menus = [dict(row) for row in cur.fetchall()]
            return menus
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []

def get_menus_for_restaurant(restaurant_id):
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, title FROM menus WHERE restaurant_id=?",(restaurant_id,))
            menus = [dict(row) for row in cur.fetchall()]
            print(menus)
            return menus
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []

@app.route('/get_menus')
def get_menus():
    restaurant_id = request.args.get('restaurant_id')
    # Fetch menu options based on the selected restaurant_id (replace with your logic)
    menus = get_menus_for_restaurant(restaurant_id)
    
    # Generate HTML options for the menus
    menu_options = ''.join([f'<option value="{menu["id"]}">{menu["title"]}</option>' for menu in menus])
    
    return menu_options

# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/enternew", methods=['GET', 'POST'])
def enternew():
    try:
        # Fetch restaurant types when loading the form
        restaurant_types = get_all_restaurant_types()
        if request.method == 'POST':
            # If it's a POST request, it means the form is submitted
            name = request.form['name']
            restaurant_type_id = request.form.get('restaurant_type_id')
            min_cost = request.form['min_cost']
            rating = request.form['rating']
            is_free_delivery = request.form.get('is_free_delivery', 0)
            delivery_time = request.form['delivery_time']
            cost_level = request.form['cost_level']
            status = request.form['status']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO restaurants (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status))

                con.commit()
                msg = "Record successfully added to the database"
                restaurant_types = get_all_restaurant_types()

                return render_template('result.html', msg=msg, restaurant_types=restaurant_types)

        return render_template("restaurant.html", restaurant_types=restaurant_types)

    except Exception as e:
        print(f"Error in enternew: {str(e)}")
        return render_template("restaurant.html", restaurant_types=[])
    
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    try:
        if request.method == 'POST':
            # Get form data
            user_id = request.form['user_id']
            restaurant_id = int(request.form.get('restaurant_id'))
            menu_id = int(request.form.get('menu_id'))
            amount = int(request.form['amount'])
            if not is_user_id_exist(user_id):
                raise ValueError("User id does not exist.")
            elif amount == 0:
                raise ValueError("Amount should be greater than 0.")
            else:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO orders (user_id, restaurant_id, menu_id, amount, created_at) VALUES (?, ?, ?, ?, ?)",
                                (user_id, restaurant_id, menu_id, amount, datetime.now()))

                    con.commit()
                    msg = "Record successfully added to the database"
                    return render_template('result.html', msg=msg, restaurants=get_all_restaurants())

        return render_template("add_order.html", restaurants=get_all_restaurants())
    except Exception as e:
        error_message = str(e)
        return render_template("add_order.html", error_message=error_message,restaurants=get_all_restaurants())
       
    
@app.route("/add_menu", methods=['GET', 'POST'])
def add_menu():
    try:
        # Fetch restaurant types when loading the form
        restaurants = get_all_restaurants()
        if request.method == 'POST':
            # If it's a POST request, it means the form is submitted
            title = request.form['title']
            price = request.form.get('price')
            description = request.form['description']
            restaurant_id = request.form.get('restaurant_id')
            print(restaurants)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT restaurant_type_id FROM restaurants WHERE id=?",(restaurant_id,))
                food_type_id = cur.fetchone()[0]
                print(food_type_id)
                cur.execute("INSERT INTO menus ( title , price , description , restaurant_id , food_type_id , created_at)  VALUES (?, ?, ?, ?, ?, ?)",
                            (title, price, description, restaurant_id, food_type_id, datetime.now()))

                con.commit()
                msg = "Record successfully added to the database"

                return render_template('result.html', msg=msg, restaurants=restaurants)

        return render_template("add_menu.html", restaurants=restaurants)

    except Exception as e:
        print(f"Error in add menu: {str(e)}")
        return render_template("add_menu.html", restaurants=restaurants)
    

    
@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            # If it's a POST request, it means the form is submitted
            email = request.form['email']
            user_name = request.form.get('user_name')
            password = request.form['password']
            name = request.form['name']
            surname = request.form.get('surname')
            password = generate_password_hash(password)
            if is_email_exist(email):
                raise ValueError("Email already exists")
            elif is_user_exist(user_name):
                raise ValueError("Username already exists")
            elif len(email) < 4:
                raise ValueError("Email must be greater than 3 characters.")
            elif len(name) < 2:
                raise ValueError("First name must be greater than 1 character.")
            else:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO users ( email , password , user_name , name , surname , created_at ) VALUES ( ?, ?, ?, ?, ?, ?)",
                                (email, password, user_name, name, surname, datetime.now()))

                    con.commit()
                    msg = "Record successfully added to the database"

                    return render_template('result.html', msg=msg)

        return render_template("add_user.html")

    except Exception as e:
        error_message = str(e)
        return render_template("add_user.html", error_message=error_message)

@app.route("/enternewtype", methods=['GET', 'POST'])
def enternewtype():
    try:
        if request.method == 'POST':
            type_name = request.form['type_name']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                # Check if the restaurant type already exists
                cur.execute("SELECT id FROM restaurant_type WHERE type=?", (type_name,))
                existing_type = cur.fetchone()

                if existing_type:
                    raise ValueError("Restaurant type already exists")

                # Insert the restaurant type if it doesn't exist
                cur.execute("INSERT INTO restaurant_type (type) VALUES (?)", (type_name,))

                con.commit()
                msg = "Restaurant type successfully added to the database"
                return render_template('result.html', msg=msg)

        return render_template("restaurant_type.html")

    except Exception as e:
        error_msg = str(e) if str(e) else "Error adding restaurant type"
        return render_template("restaurant_type.html", error_msg=error_msg)


# Route to SELECT all data from the database and display in a table      
@app.route('/list_restaurants2/', methods=['GET'])
def list_restaurants2():
    try:
        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        restaurants = get_all_restaurants(sort_by, order)
        return render_template("list_restaurants.html", restaurants=restaurants)
    except ValueError as e:
        return str(e)
    
@app.route('/list_menus/', defaults={'page': 1}, methods=['GET'])
@app.route('/list_menus/<int:page>', methods=['GET'])
def list_menus(page):
    try:
        per_page = 20  # Number of menus per page

        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'title', 'price', 'restaurant_id', 'food_type_id']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        # Get the menus for the specified page with ordering
        menus = get_menus_for_page(page, per_page, sort_by, order)

        # Get the total number of menus for pagination
        total_menus = get_total_menus()

        # Calculate the total number of pages
        total_pages = ((total_menus) // per_page) + 1

        return render_template(
            "list_menus.html",
            menus=menus,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        return str(e)

@app.route('/list_orders2')
def list_orders2():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT orders.id as id, orders.user_id as user_id, restaurants.name as restaurant_name, menus.title as menu_title, orders.amount as amount FROM orders left join restaurants on restaurants.id = orders.restaurant_id left join menus on menus.id = orders.menu_id order by orders.id")

    orders = cur.fetchall()
    print(orders)
    con.close()
    return render_template("list_orders.html",orders=orders)

# Add this route to your app
@app.route("/listtypes")
def list_types():
    restaurant_types = get_all_restaurant_types()
    return render_template("list_types.html", restaurant_types=restaurant_types)

@app.route('/list_users')
def list_users():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    con.close()
    return render_template("list_users.html", users=rows)

@app.route("/edit_order", methods=['POST', 'GET'])
def edit_order():
    
    con = sqlite3.connect("database.db")
    try:
        id = request.form['order_id']
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT orders.restaurant_id as restaurant_id, orders.id as id, orders.user_id as user_id, restaurants.name as restaurant_name, menus.title as menu_title, orders.amount as order_amount FROM orders, restaurants, menus WHERE restaurants.id = orders.restaurant_id AND menus.id = orders.menu_id AND orders.id = ?", (id,))

        order = cur.fetchone()
        print(order)
        con.close()
        return render_template("edit_order.html", order=order,restaurants=get_all_restaurants(), menus=get_all_menus())
    except Exception as e:
        print(f"Error in the SELECT: {str(e)}")
        return render_template("edit_order.html", restaurants=get_all_restaurants(), menus=get_all_menus())


@app.route('/edit_order_rec', methods=['POST','GET'])
def edit_order_rec():
    if request.method == 'POST':
        con = None  # Initialize con outside the try block
        try:
            id = request.form['id']
            name = request.form['name']
            restaurant_type_id = request.form['restaurant_type_id']
            min_cost = request.form['min_cost']
            rating = request.form['rating']
            is_free_delivery = request.form['is_free_delivery']
            delivery_time = request.form['delivery_time']
            cost_level = request.form['cost_level']
            status = request.form['status']

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE restaurants SET name=?, restaurant_type_id=?, min_cost=?, rating=?, is_free_delivery=?, delivery_time=?, cost_level=?, status=? WHERE id=?",
                        (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status, id))

            con.commit()
            msg = "Record successfully edited in the database"
        except Exception as e:
            if con:
                con.rollback()
            msg = f"Error in the Edit: {str(e)}"
        finally:
            if con:
                con.close()
            return render_template('result.html', msg=msg)

# For delete_order, you can use a similar approach:
@app.route('/delete_order', methods=['POST'])
def delete_order():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM orders WHERE id=?", (id,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except Exception as e:
            con.rollback()
            msg = f"Error in the DELETE: {str(e)}"
        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM restaurants WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_restaurants.html", restaurants=rows, restaurant_types=get_all_restaurant_types())
        
@app.route("/edit_menu", methods=['POST', 'GET'])
def edit_menu():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM menus WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_menu.html", menus=rows, restaurant_types=get_all_restaurant_types(), restaurants=get_all_restaurants())
        
@app.route("/edit_menu_rec", methods=['POST', 'GET'])
def edit_menu_rec():
     if request.method == 'POST':
        con = None  # Initialize con outside the try block
        try:
            id = request.form['id']
            title = request.form['title']
            restaurant_id = request.form['restaurant_id']
            price = request.form['price']
            description = request.form['description']
            food_type_id = request.form.get('food_type_id')

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE menus SET title=?, restaurant_id=?, price=?, description=?, food_type_id=? WHERE id=?",
                        (title, restaurant_id, price, description, food_type_id, id))

            con.commit()
            msg = "Record successfully edited in the database"
        except Exception as e:
            if con:
                con.rollback()
            msg = f"Error in the Edit: {str(e)}"
        finally:
            if con:
                con.close()
            return render_template('result.html', msg=msg)


# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST', 'GET'])
def editrec():
    if request.method == 'POST':
        con = None  # Initialize con outside the try block
        try:
            id = request.form['id']
            name = request.form['name']
            restaurant_type_id = request.form['restaurant_type_id']
            min_cost = request.form['min_cost']
            rating = request.form['rating']
            is_free_delivery = request.form['is_free_delivery']
            delivery_time = request.form['delivery_time']
            cost_level = request.form['cost_level']
            status = request.form['status']

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE restaurants SET name=?, restaurant_type_id=?, min_cost=?, rating=?, is_free_delivery=?, delivery_time=?, cost_level=?, status=? WHERE id=?",
                        (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status, id))

            con.commit()
            msg = "Record successfully edited in the database"
        except Exception as e:
            if con:
                con.rollback()
            msg = f"Error in the Edit: {str(e)}"
        finally:
            if con:
                con.close()
            return render_template('result.html', msg=msg)


# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM restaurants WHERE id=?", (id,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except Exception as e:
            con.rollback()
            msg = f"Error in the DELETE: {str(e)}"
        finally:
            con.close()
            return render_template('result.html', msg=msg)
    
# Route used to DELETE a specific record in the database    
@app.route("/delete_menu", methods=['POST', 'GET'])
def delete_menu():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM menus WHERE id=?", (id,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except Exception as e:
            con.rollback()
            msg = f"Error in the DELETE: {str(e)}"
        finally:
            con.close()
            return render_template('result.html', msg=msg)
        

@app.route("/edit_type", methods=['POST', 'GET'])
def edit_type():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM restaurant_type WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_type.html", restaurant_types=rows)



@app.route("/edit_type_rec", methods=['POST'])
def edit_type_rec():
    try:
        id = request.form['id']
        new_type_name = request.form['type']

        # Check if the new type already exists
        if not is_type_exist(new_type_name):
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE restaurant_type SET type=? WHERE id=?", (new_type_name, id))
                con.commit()
                msg = "Restaurant Type successfully edited in the database"
                return render_template('result.html', msg=msg)
        else:
            msg = "Error: Restaurant Type already exists"
            return render_template('result.html', msg=msg)
    except Exception as e:
        msg = f"Error in the Edit: {str(e)}"
        return render_template('result.html', msg=msg)





# Route to handle deleting a restaurant type
@app.route("/deletetype", methods=['POST'])
def deletetype():
    if request.method == 'POST':
        try:
            id = request.form['id']

            # Delete the related restaurants first
            delete_related_restaurants(id)

            # Now, delete the type from the database
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM restaurant_type WHERE id=?", (id,))
                con.commit()
                msg = "Restaurant type successfully deleted from the database"
        except Exception as e:
            msg = f"Error in deleting restaurant type: {str(e)}"
        finally:
            return redirect("/list_types")  # Redirect to the listtypes page

def delete_related_restaurants(type_id):
    # Delete related restaurants from the database
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM restaurants WHERE restaurant_type_id=?", (type_id,))
        con.commit()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            user_name = request.form['userName']
            password1 = request.form['password1']
            password2 = request.form['password2']
            
            
            if is_email_exist(email):
                raise ValueError("Email already exists")
            elif is_user_exist(user_name):
                raise ValueError("Username already exists")
            elif len(email) < 4:
                raise ValueError("Email must be greater than 3 characters.")
            elif len(first_name) < 2:
                raise ValueError("First name must be greater than 1 character.")
            elif password1 != password2:
                raise ValueError("Passwords don\'t match.")
            elif len(password1) < 7:
                raise ValueError("Password must be at least 7 characters.")
            else:
                password1 = generate_password_hash(password1)
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO users (email, name, surname, user_name, password, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                (email, first_name, last_name, user_name, password1, datetime.now()))
                    con.commit()

            msg = "User successfully signed up."
            return render_template('result.html', msg=msg)

        except Exception as e:
            error_message =  str(e)
            return render_template('signup.html', error_message=error_message)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            if is_email_exist(email):
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("SELECT password FROM users WHERE email=?", (email,))
                    originalPass = cur.fetchone()
                if check_password_hash(originalPass, password):
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('/')) 
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
            return redirect('/')  
        except Exception as e:
            error_message = f"Error during login: {str(e)}"
            return render_template('login.html', error_message=error_message)        

    return render_template("login.html", user=current_user)



@app.route("/edit_user", methods=['POST', 'GET'])
def edit_user():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_user.html", users=rows)

@app.route("/edit_user_rec", methods=['POST', 'GET'])
def edit_user_rec():
    if request.method == 'POST':
        con = None  # Initialize con outside the try block
        try:
            id = request.form['id']
            email = request.form['email']
            user_name = request.form.get('user_name')
            password = request.form['password']
            name = request.form['name']
            surname = request.form.get('surname')
            password = generate_password_hash(password)

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE users SET email=?, password=?, user_name=?, name=?, surname=?, created_at=? WHERE id=?",
                        (email, password, user_name, name, surname, datetime.now(), id))

            con.commit()
            msg = "Record successfully edited in the database"
        except Exception as e:
            if con:
                con.rollback()
            msg = f"Error in the Edit: {str(e)}"
        finally:
            if con:
                con.close()
            return render_template('result.html', msg=msg)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        user_id = request.form['id']

        # Perform the delete operation in the database
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id=?", (user_id,))
            con.commit()

        return redirect(url_for('list_users'))

    except Exception as e:
        print(f"Error in delete_user: {str(e)}")
        return redirect(url_for('list_users'))


def get_restaurants_for_page(page, per_page, sort_by, order):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    # Calculate the offset based on the page number and number of restaurants per page
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT restaurants.*, restaurant_type.type as restaurant_type FROM restaurants left join restaurant_type on restaurant_type.id = restaurants.restaurant_type_id  ORDER BY {sort_by} {order} LIMIT ? OFFSET ?", (per_page, offset))
        restaurants = cur.fetchall()

    return restaurants

def get_total_restaurants():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM restaurants")
        total_restaurants = cur.fetchone()[0]

    return total_restaurants

@app.route('/list_restaurants/', defaults={'page': 1}, methods=['GET'])
@app.route('/list_restaurants/<int:page>', methods=['GET'])
def list_restaurants(page):
    try:
        per_page = 20  # Number of restaurants per page

        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        # Get the restaurants for the specified page with ordering
        restaurants = get_restaurants_for_page(page, per_page, sort_by, order)

        # Get the total number of restaurants for pagination
        total_restaurants = get_total_restaurants()

        # Calculate the total number of pages
        total_pages = ((total_restaurants) // per_page) + 1

        return render_template(
            "list_restaurants.html",
            restaurants=restaurants,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order,
        )
    except Exception as e:
        return str(e)

def get_orders_for_page(page, per_page, sort_by, order):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'user_id', 'restaurant_id', 'menu_id', 'amount', 'created_at']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    # Calculate the offset based on the page number and number of orders per page
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT orders.id as id, orders.user_id as user_id, restaurants.name as restaurant_name, menus.title as menu_title, orders.amount as amount, orders.created_at as created_at FROM orders left join restaurants on restaurants.id = orders.restaurant_id left join menus on menus.id = orders.menu_id ORDER BY {sort_by} {order} LIMIT ? OFFSET ?", (per_page, offset))
        orders = cur.fetchall()

    return orders

def get_total_orders():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM orders")
        total_orders = cur.fetchone()[0]

    return total_orders

@app.route('/list_orders/', defaults={'page': 1}, methods=['GET'])
@app.route('/list_orders/<int:page>', methods=['GET'])
def list_orders(page):
    try:
        per_page = 20  # Number of orders per page

        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'user_id', 'restaurant_id', 'menu_id', 'amount', 'created_at']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        # Get the orders for the specified page with ordering
        orders = get_orders_for_page(page, per_page, sort_by, order)

        # Get the total number of orders for pagination
        total_orders = get_total_orders()

        # Calculate the total number of pages
        total_pages = ((total_orders) // per_page) + 1

        return render_template(
            "list_orders.html",
            orders=orders,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order,
        )
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
