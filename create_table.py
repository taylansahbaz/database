# Author: Rasim Berke Turan, Istanbul Technical University
# Date: 12/21/2023

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

with sqlite3.connect('database.db') as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS restaurant_type (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT)")
    con.commit()

conn.execute('CREATE TABLE IF NOT EXISTS restaurants (id INTEGER PRIMARY KEY, name TEXT, restaurant_type_id INTEGER, min_cost INTEGER, rating FLOAT, is_free_delivery BOOLEAN, delivery_time VARCHAR, cost_level INTEGER, status INTEGER, created_at TIMESTAMP, FOREIGN KEY (restaurant_type_id) REFERENCES restaurant_type(id) ON DELETE CASCADE)')
print("Table restaurants created successfully!")

conn.execute('CREATE TABLE IF NOT EXISTS menus (id INTEGER PRIMARY KEY, title VARCHAR, price FLOAT, description TEXT, restaurant_id INTEGER, food_type_id INTEGER, created_at TIMESTAMP, FOREIGN KEY (restaurant_id) REFERENCES restaurants(id), FOREIGN KEY (food_type_id) REFERENCES food_type(id))')
print("Table menus created successfully!")

conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email VARCHAR UNIQUE, password VARCHAR, user_name VARCHAR, name VARCHAR, surname VARCHAR, created_at TIMESTAMP)')
print("Table users created successfully!")

conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, restaurant_id INTEGER, menu_id INTEGER, amount INTEGER, created_at TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (restaurant_id) REFERENCES restaurants(id), FOREIGN KEY (menu_id) REFERENCES menus(id))')
print("Table orders created successfully!")


conn.close()

