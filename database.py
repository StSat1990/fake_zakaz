import sqlite3
from datetime import datetime

db = sqlite3.connect('dostavka.db')

fake_evos = db.cursor()

fake_evos.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, phone_number TEXT, address TEXT,'
                  'reg_date DATETIME);')
fake_evos.execute('CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_price REAL, '
                  'pr_quantity INTEGER, pr_desc TEXT, pr_photo TEXT, date DATETIME);')
fake_evos.execute('CREATE TABLE IF NOT EXISTS user_cart (user_id INTEGER, user_product INTEGER, quantity INTEGER, '
                  'total_for_price REAL);')

def register_user(tg_id, name, phone_number, adress):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    fake_evos.execute('INSERT INTO users (tg_id, name, phone_number, address, reg_date) '
                      'VALUES (?, ?, ?, ?, ?)', (tg_id, name, phone_number, adress, datetime.now()))
    db.commit()

def check_user(user_id):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    checker = fake_evos.execute('SELECT tg_id FROM users WHERE tg_id = ?;', (user_id,))

    if checker.fetchone():
        return True
    else:
        return False

def add_products(pr_name, pr_price, pr_quantity, pr_desc, pr_photo):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    pr = fake_evos.execute('SELECT * FROM products WHERE pr_name=?;', (pr_name,))

    if pr.fetchone():
        pass
    else:
        fake_evos.execute ('INSERT INTO products (pr_name, pr_price, pr_quantity, pr_desc, pr_photo, date) '
                      'VALUES (?, ?, ?, ?, ?, ?)', (pr_name, pr_price, pr_quantity, pr_desc, pr_photo, datetime.now()))
    db.commit()

def chek_product(pr_name):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()
    check_product = fake_evos.execute('SELECT pr_name FROM products WHERE pr_name = ?;', (pr_name,))

    if check_product.fetchone():
        return True
    else:
        return False


def get_pr_name_id():
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    products = fake_evos.execute('SELECT pr_name, pr_id, pr_quantity FROM products;').fetchall()

    sorted_products = [(i[0], i[1]) for i in products if i[2] > 0]

    return sorted_products

def get_pr_id():
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    products = fake_evos.execute('SELECT pr_name, pr_id, pr_quantity FROM products;').fetchall()

    sorted_products = [(i[1]) for i in products if i[2] > 0]

    return sorted_products

def get_product_id(pr_id):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    product_id = fake_evos.execute('SELECT pr_name, pr_desc, pr_photo, pr_price FROM products '
                                   'WHERE pr_id=?;', (pr_id,)).fetchone()
    return product_id

def add_product_to_cart(user_id, user_product, quantity):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    product_price = get_product_id(user_product)[3]

    fake_evos.execute('INSERT INTO user_cart (user_id, user_product, quantity, total_for_price) VALUES (?, ?, ?, ?);',
                      (user_id, user_product, quantity, quantity * product_price))

    db.commit()

def del_product_from_cart(user_id):
    db = sqlite3.connect('dostavka.db')

    fake_evos = db.cursor()

    fake_evos.execute('DELETE FROM user_cart WHERE user_id=?;', (user_id,))
    db.commit()

def user_cart(user_id):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    user_cart = sql.execute('SELECT products.pr_name, user_cart.quantity, user_cart.total_for_price FROM products INNER JOIN user_cart ON products.pr_id=user_cart.user_product WHERE user_cart.user_id=?;',
                            (user_id,)).fetchall()
    print(user_cart)

    return user_cart

def get_user_number_name(user_id):
    connection = sqlite3.connect('dostavka.db')
    sql = connection.cursor()

    exact_user = sql.execute('SELECT name, phone_number FROM users WHERE tg_id=?;', (user_id,))

    # print(exact_user.fetchone())
    return exact_user.fetchone()
