from flask import Blueprint, request, jsonify
import time
import logging
from database import get_db_connection
from generate_event_tracking_data import DataGenerator
from flask_jwt_extended import jwt_required, get_jwt_identity
from data_routing import DataRouter
from azure.storage.blob import BlobServiceClient
from utils import NoProxy
from config import Config

data_bp = Blueprint('data', __name__)
gd = DataGenerator()
# Pass connection string explicitly to ensure QueueClient works outside Azure Functions host
router = DataRouter(Config.AZURE_STORAGE_CONNECTION_STRING)

@data_bp.route('/write_to_db', methods=['POST'])
@jwt_required()
def write_to_db():
    connection = None
    try:
        connection = get_db_connection()
        data = request.get_json()
        data_count = int(data['dataCount'])
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

            def append_data(user, address, category, subcategory, product, products_sku, payment, order, wishlist, order_item):
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
                py_end = time.perf_counter()

                append_data(user, address, category, subcategory, product, products_sku, payment, order, wishlist, order_item)
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


@data_bp.route('/clean_data', methods=['POST'])
@jwt_required()
def clean_data():
    """
    V1.0 Route: Submit data for cleaning and loading via Azure Data Factory
    
    Implements dual-path ETL:
    - Small Batch (<=10k records): Fast Path via Pandas + Azure Function (10-min ADF trigger)
    - Large Batch (>10k records): Heavy Path via PySpark + Databricks (daily ADF trigger)
    
    Request JSON:
    {
        "dataCount": 5000,  # Number of records to generate and clean
        "jobName": "Q4_2024_Sales" # Optional job name
    }
    
    Response:
    {
        "success": true,
        "jobId": "uuid",
        "parentJobId": "uuid",
        "processingPath": "small_batch" | "large_batch",
        "queueName": "small-batch-queue" | "large-batch-queue",
        "expectedProcessingTime": "<5 minutes (10-min ADF trigger)" | "<24 hours (daily ADF trigger)",
        "message": "Data routing decision and queue message details"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        data_count = int(data['dataCount'])
        parent_job_id = data.get('parentJobId')
        # Fetch jobIds from blob storage
        with NoProxy():
            container_client = BlobServiceClient.from_connection_string(
                Config.AZURE_STORAGE_CONNECTION_STRING
            ).get_container_client('shanlee-raw-data')
            
            blobs = list(container_client.list_blobs(name_starts_with=f"{user_id}/{parent_job_id}/"))
            job_ids = [blob.name.split('/')[-1].replace('.json', '') for blob in blobs]
        
        # Queue one message per chunk for parallel processing
        queue_name = None
        for job_id in job_ids:
            queue_name = router.queue_message_to_path(
                user_id=user_id,
                count=data_count,
                job_id=job_id,
                parent_job_id=parent_job_id,
                total_jobs=len(job_ids)
            )
        
        # All chunks routed to same queue (based on count), so get decision once
        processing_path = 'small_batch' if data_count <= 10000 else 'large_batch'
        expected_time = '<5 minutes (10-min ADF trigger)' if data_count <= 10000 else '<24 hours (daily ADF trigger)'
        
        logging.info(f"Cleaning queued: {len(job_ids)} chunks to {queue_name}, path={processing_path}")
        
        return jsonify({
            'success': True,
            'parentJobId': parent_job_id,
            'jobIds': job_ids,
            'totalChunks': len(job_ids),
            'processingPath': processing_path,
            'queueName': queue_name,
            'expectedProcessingTime': expected_time,
            'recordCount': data_count,
            'message': f'{len(job_ids)} chunks queued to {queue_name}'
        })
    
    except Exception as e:
        logging.error(f"Error in clean_data endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing request: {str(e)}'
        }), 500


@data_bp.route('/get_<table_name>', methods=['GET'])
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
        'order_item': 'order_item'
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
        connection = get_db_connection()
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
