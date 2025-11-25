from flask import Flask, jsonify, request
import time
from flask_cors import CORS
import pymysql
import socks
import socket
from dbutils.pooled_db import PooledDB
from generate_event_tracking_data import DataGenerator
import os
from dotenv import load_dotenv
import logging
import uuid
from azure.storage.queue import QueueClient
from azure.storage.blob import BlobServiceClient
import json
import base64
load_dotenv()

# Save the original socket class to bypass proxy later if needed
original_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7890)  # Clash 的本地代理端口
socket.socket = socks.socksocket

# Context manager to temporarily disable proxy
class NoProxy:
    def __enter__(self):
        self.patched_socket = socket.socket
        socket.socket = original_socket
    
    def __exit__(self, exc_type, exc_value, traceback):
        socket.socket = self.patched_socket

# azure mysql 连接配置
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
CORS(app)  # Enable CORS for frontend communication

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/write_to_db', methods=['POST'])
def write_to_db():
    connection = None
    try:
        connection = pool.connection()
        data = request.get_json(silent=True) or {}
        data_count = int(data.get('dataCount', 1))
        messages = []
        user_ids = []
        with connection.cursor() as cursor:
            sql_total_time = 0
            python_total_time = 0
            # Prepare lists for each table
            users = []
            addresses = []
            categories = []
            subcategories = []
            products = []
            products_skus = []
            payments = []
            orders = []
            wishlists = []
            order_items = []
            carts = []

            def append_data(user, address, category, subcategory, product, products_sku, payment, order, wishlist, order_item, cart):
                users.append((user['id'], user['username'], user['real_name'], user['phone_number'], user['sex'], user['job'], user['company'], user['email'], user['password'], user['birth_of_date'], user['age'], user['create_time'], user['delete_time']))
                addresses.append((address['id'], address['user_id'], address['title'], address['address_line'], address['country'], address['city'], address['postal_code'], address['create_time'], address['delete_time']))
                categories.append((category['id'], category['name'], category['description'], category['create_time'], category['delete_time']))
                subcategories.append((subcategory['id'], subcategory['parent_id'], subcategory['name'], subcategory['description'], subcategory['create_time'], subcategory['delete_time']))
                products.append((product['id'], product['name'], product['description'], product['category_id'], product['create_time'], product['delete_time']))
                products_skus.append((products_sku['id'], products_sku['product_id'], products_sku['price'], products_sku['quantity'], products_sku['create_time'], products_sku['delete_time']))
                payments.append((payment['id'], payment['amount'], payment['provider'], payment['status'], payment['create_time'], payment['updated_at']))
                orders.append((order['id'], order['user_id'], order['payment_id'], order['create_time'], order['updated_at']))
                wishlists.append((wishlist['id'], wishlist['user_id'], wishlist['products_sku_id'], wishlist['create_time'], wishlist['delete_time']))
                order_items.append((order_item['id'], order_item['order_id'], order_item['products_sku_id'], order_item['quantity'], order_item['create_time'], order_item['updated_at']))
                carts.append((cart['id'], cart['order_id'], cart['products_sku_id'], cart['quantity'], cart['create_time'], cart['updated_at']))

            for _ in range(data_count):
                py_start = time.perf_counter()
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
                py_end = time.perf_counter()

                append_data(user, address, category, subcategory, product, products_sku, payment, order, wishlist, order_item, cart)
                messages.append(f"your user name is : {user['username']}")
                user_ids.append(user['id'])
                python_total_time += (py_end - py_start)

            import time as _time
            sql_start = _time.perf_counter()
            cursor.executemany("INSERT INTO users (id, user_name, real_name, phone_number, sex, job, company, email, password, birth_of_date, age, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", users)
            cursor.executemany("INSERT INTO addresses (id, user_id, title, address_line, country, city, postal_code, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", addresses)
            cursor.executemany("INSERT INTO categories (id, name, description, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s)", categories)
            cursor.executemany("INSERT INTO sub_categories (id, parent_id, name, description, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s)", subcategories)
            cursor.executemany("INSERT INTO products (id, name, description, category_id, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s)", products)
            cursor.executemany("INSERT INTO products_skus (id, product_id, price, stock, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s, %s)", products_skus)
            cursor.executemany("INSERT INTO payment_details (id, amount, provider, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", payments)
            cursor.executemany("INSERT INTO order_details (id, user_id, payment_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)", orders)
            cursor.executemany("INSERT INTO wishlist (id, user_id, products_sku_id, created_at, deleted_at) VALUES (%s, %s, %s, %s, %s)", wishlists)
            cursor.executemany("INSERT INTO order_item (id, order_id, products_sku_id, quantity, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", order_items)
            cursor.executemany("INSERT INTO cart (id, order_id, products_sku_id, quantity, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", carts)
            connection.commit()
            sql_end = _time.perf_counter()
            sql_total_time = sql_end - sql_start
            logging.info(f'sql time {sql_total_time:.4f}s, python time: {python_total_time:.4f}s')

        return jsonify({
            'success': True,
            'message': messages[-1] if messages else '',
            'user_id': user_ids[-1] if user_ids else None,
            'all_messages': messages,
            'all_user_ids': user_ids,
            'generation_time': python_total_time,
            'commit_time': sql_total_time
        })

    except Exception as e:
        logging.error(f"数据库操作失败: {str(e)}")
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
            select_query = f"SELECT * FROM {db_table_name} ORDER BY created_at DESC LIMIT 20"
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

@app.route('/generate_raw', methods=['POST'])
def generate_job():
    data = request.get_json()
    total_count = data.get('dataCount', 1)
    batch_size = 1000  # You can adjust this value as needed

    parent_job_id = str(uuid.uuid4())
    job_ids = []
    # Enqueue job to Azure Queue
    # Use NoProxy context to bypass SOCKS5 proxy for Azure SDK
    with NoProxy():
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        queue_name = 'data-generation-queue'
        queue_client = QueueClient.from_connection_string(connection_string, queue_name)
        print('queue client created---------------------')
        for start in range(0, total_count, batch_size):
            count = min(batch_size, total_count - start)
            job_id = str(uuid.uuid4())
            message = {'parentJobId': parent_job_id, 'jobId': job_id, 'count': count}
            encoded_message = base64.b64encode(json.dumps(message).encode('utf-8')).decode('utf-8')
            queue_client.send_message(encoded_message)
            print(f'message for chunk {job_id} has sent---------------------')
            job_ids.append(job_id)

    print('all chunk messages have been sent---------------------')
    return jsonify({
        'parentJobId': parent_job_id,
        'jobIds': job_ids,
        'status': 'queued',
        'total_count': total_count,
        'batch_size': batch_size
    }), 202

@app.route('/get_raw_data/<job_id>', methods=['GET'])
def get_raw_data(job_id):
    try:
        with NoProxy():
            connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_name = 'raw-generated-data'
            blob_name = f'{job_id}.json'
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            
            if not blob_client.exists():
                return jsonify({'success': False, 'message': 'Data not found or not ready yet'}), 404
                
            blob_data = blob_client.download_blob().readall()
            data = json.loads(blob_data)
            
            return jsonify({
                'success': True,
                'data': data
            })
    except Exception as e:
        logging.error(f"Error retrieving raw data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving data: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)