from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
from pymysql import cursors
from pymysql.connections import Connection
from dbutils.pooled_db import PooledDB
from generate_event_tracking_data import DataGenerator
import os
from dotenv import load_dotenv
load_dotenv()

# 阿里云 RDS 连接配置
config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ['DB_PORT']),
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'database': os.environ['DB_NAME'],
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Create a connection pool for better performance
pool = PooledDB(
    creator=pymysql,
    maxconnections=6,
    mincached=2,
    maxcached=5,
    maxshared=3,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    **config
)

gd = DataGenerator()


app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

@app.route('/write_to_db', methods=['POST'])
def write_to_db():
    connection = None
    try:
        # Use connection pool for better performance
        connection = pool.connection()
        
        # Generate all data first
        user = gd.generate_user_data()
        address = gd.generate_fake_address(user)
        category = gd.generate_categories_data()
        subcategory = gd.generate_subcategories_data(category)
        product = gd.generate_products_data(subcategory)
        products_sku = gd.generate_sku_data(category,subcategory,product)
        wishlist = gd.generate_wishlist_data(products_sku,user)
        payment = gd.generate_payment_details_data()
        order = gd.generate_order_details_data(user,payment)
        order_item = gd.generate_order_item_data(products_sku,order)
        cart = gd.generate_cart_data(products_sku,order)
        
        with connection.cursor() as cursor:
            # Use executemany for batch inserts where possible
            # For single row inserts, we can still optimize by preparing all queries
            
            # Prepare all insert queries and data
            queries = [
                ("INSERT INTO users (id, user_name, real_name, phone_number, sex, job, company, email, password, birth_of_date, age, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 (user['id'], user['username'], user['real_name'], user['phone_number'], user['sex'], user['job'], user['company'], user['email'], user['password'], user['birth_of_date'], user['age'], user['create_time'], user['delete_time'])),
                
                ("INSERT INTO addresses (id, user_id, title, address_line, country, city, postal_code, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 (address['id'], address['user_id'], address['title'], address['address_line'], address['country'], address['city'], address['postal_code'], address['create_time'], address['delete_time'])),
                
                ("INSERT INTO categories (id, name, description, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s)",
                 (category['id'], category['name'], category['description'], category['create_time'], category['delete_time'])),
                
                ("INSERT INTO sub_categories (id, parent_id, name, description, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s)",
                 (subcategory['id'], subcategory['parent_id'], subcategory['name'], subcategory['description'], subcategory['create_time'], subcategory['delete_time'])),
                
                ("INSERT INTO products (id, name, description, category_id, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s)",
                 (product['id'], product['name'], product['description'], product['category_id'], product['create_time'], product['delete_time'])),
                
                ("INSERT INTO products_skus (id, product_id, price, stock, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s)",
                 (products_sku['id'], products_sku['product_id'], products_sku['price'], products_sku['quantity'], products_sku['create_time'], products_sku['delete_time'])),
                
                ("INSERT INTO payment_details (id, amount, provider, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
                 (payment['id'], payment['amount'], payment['provider'], payment['status'], payment['create_time'], payment['updated_at'])),
                
                ("INSERT INTO order_details (id, user_id, payment_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                 (order['id'], order['user_id'], order['payment_id'], order['create_time'], order['updated_at'])),
                
                ("INSERT INTO wishlist (id, user_id, products_sku_id, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s)",
                 (wishlist['id'], wishlist['user_id'], wishlist['products_sku_id'], wishlist['create_time'], wishlist['delete_time'])),
                
                ("INSERT INTO order_item (id, order_id, products_sku_id, quantity, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
                 (order_item['id'], order_item['order_id'], order_item['products_sku_id'], order_item['quantity'], order_item['create_time'], order_item['updated_at'])),
                
                ("INSERT INTO cart (id, order_id, products_sku_id, quantity, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
                 (cart['id'], cart['order_id'], cart['products_sku_id'], cart['quantity'], cart['create_time'], cart['updated_at']))
            ]
            
            # Execute all queries in a single batch
            for query, data in queries:
                cursor.execute(query, data)
            
            # Commit transaction once for all inserts
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f'your user name is : {user['username']}',
                'user_id': user['id']
            })

    except Exception as e:
        print("数据库操作失败:", str(e))
        # 如果发生错误，回滚事务
        if connection:
            connection.rollback()
        return jsonify({
            'success': False,
            'message': f'数据库操作失败: {str(e)}'
        }), 500
    finally:
        if connection:
            connection.close()

@app.route('/get_<table_name>', methods=['GET'])
def get_table_data(table_name):
    # Define a mapping of table names to their actual database table names
    table_mapping = {
        'user': 'users',
        'address': 'addresses',
        'category': 'categories',
        'subcategory': 'sub_categories',
        'product': 'products',
        'products_sku': 'products_skus',
        'wishlist': 'wishlist',
        'payment': 'payment_details',
        'order': 'order_details',
        'order_item': 'order_item',
        'cart': 'cart'
    }
    
    connection = None
    try:
        # Check if the requested table exists in our mapping
        if table_name not in table_mapping:
            return jsonify({
                'success': False,
                'message': f'Invalid table name: {table_name}'
            }), 400
            
        # Get the actual table name from the mapping
        db_table_name = table_mapping[table_name]
        
        # Use connection pool
        connection = pool.connection()
        with connection.cursor() as cursor:
            # Use parameterized query to prevent SQL injection
            # Since table names cannot be parameterized, we validate against whitelist above
            select_query = f"SELECT * FROM {db_table_name} ORDER BY created_at DESC LIMIT 10"
            cursor.execute(select_query)
            data = cursor.fetchall()
            
            return jsonify({
                'success': True,
                table_name: data
            })
            
    except Exception as e:
        print("数据库操作失败:", str(e))
        return jsonify({
            'success': False,
            'message': f'数据库操作失败: {str(e)}'
        }), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)