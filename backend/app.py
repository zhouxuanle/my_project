from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
from generate_event_tracking_data import DataGenerator 

# 阿里云 RDS 连接配置
config = {
    'host': 'rm-wz9g3a41c8d17147tno.mysql.rds.aliyuncs.com',      # 替换为你的 RDS 公网地址
    'port': 3306,                                      # 默认 3306
    'user': 'zhouxuanle',                           # 替换为你的数据库用户名
    'password': 'Zxl99020',                       # 替换为你的密码
    'database': 'web-app',                             # 替换为你的数据库名
    'charset': 'utf8mb4',                              # 推荐 utf8mb4 支持 emoji
    'cursorclass': pymysql.cursors.DictCursor,         # 可选：返回字典格式结果
}
gd = DataGenerator()


app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

@app.route('/write_to_db', methods=['POST'])
def write_to_db():
    try:
        # 建立连接
        connection = pymysql.connect(**config)
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
 
            # 插入用户数据到数据库
            insert_user_query = """
            INSERT INTO users (id, user_name, real_name, phone_number, sex, job, company, email, password, birth_of_date, age, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_user_query, (
                user['id'],
                user['username'],
                user['real_name'],
                user['phone_number'],
                user['sex'],
                user['job'],
                user['company'],
                user['email'],
                user['password'],
                user['birth_of_date'],
                user['age'],
                user['create_time'],
                user['delete_time']
            ))
            
            # 插入地址数据到数据库
            insert_address_query = """
            INSERT INTO addresses (id, user_id, title, address_line, country, city, postal_code, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_address_query, (
                address['id'],
                address['user_id'],
                address['title'],
                address['address_line'],
                address['country'],
                address['city'],
                address['postal_code'],
                address['create_time'],
                address['delete_time']
            ))
            
            # 插入分类数据到数据库
            insert_category_query = """
            INSERT INTO categories (id, name, description, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_category_query, (
                category['id'],
                category['name'],
                category['description'],
                category['create_time'],
                category['delete_time']
            ))
            
            # 插入子分类数据到数据库
            insert_subcategory_query = """
            INSERT INTO sub_categories (id, parent_id, name, description, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_subcategory_query, (
                subcategory['id'],
                subcategory['parent_id'],
                subcategory['name'],
                subcategory['description'],
                subcategory['create_time'],
                subcategory['delete_time']
            ))
            
            # 插入产品数据到数据库
            insert_product_query = """
            INSERT INTO products (id, name, description, category_id, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_product_query, (
                product['id'],
                product['name'],
                product['description'],
                product['category_id'],
                product['create_time'],
                product['delete_time']
            ))
            
            # 插入产品SKU数据到数据库
            insert_sku_query = """
            INSERT INTO products_skus (id, product_id, price, stock, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_sku_query, (
                products_sku['id'],
                products_sku['product_id'],
                products_sku['price'],
                products_sku['quantity'],
                products_sku['create_time'],
                products_sku['delete_time']
            ))
            
            # 插入支付详情数据到数据库
            insert_payment_query = """
            INSERT INTO payment_details (id, amount, provider, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_payment_query, (
                payment['id'],
                payment['amount'],
                payment['provider'],
                payment['status'],
                payment['create_time'],
                payment['updated_at']
            ))
            
            # 插入订单详情数据到数据库
            insert_order_query = """
            INSERT INTO order_details (id, user_id, payment_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_order_query, (
                order['id'],
                order['user_id'],
                order['payment_id'],
                order['create_time'],
                order['updated_at']
            ))
            
            # 插入心愿单数据到数据库
            insert_wishlist_query = """
            INSERT INTO wishlist (id, user_id, products_sku_id, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_wishlist_query, (
                wishlist['id'],
                wishlist['user_id'],
                wishlist['products_sku_id'],
                wishlist['create_time'],
                wishlist['delete_time']
            ))
            
            # 插入订单项数据到数据库
            insert_order_item_query = """
            INSERT INTO order_item (id, order_id, products_sku_id, quantity, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_order_item_query, (
                order_item['id'],
                order_item['order_id'],
                order_item['products_sku_id'],
                order_item['quantity'],
                order_item['create_time'],
                order_item['updated_at']
            ))
            
            # 插入购物车数据到数据库
            insert_cart_query = """
            INSERT INTO cart (id, order_id, products_sku_id, quantity, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_cart_query, (
                cart['id'],
                cart['order_id'],
                cart['products_sku_id'],
                cart['quantity'],
                cart['create_time'],
                cart['updated_at']
            ))
            
            # 提交事务
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f'your user name is : {user['username']}',
                'user_id': user['id']
            })

    except Exception as e:
        print("数据库操作失败:", str(e))
        # 如果发生错误，回滚事务
        if 'connection' in locals():
            connection.rollback()
        return jsonify({
            'success': False,
            'message': f'数据库操作失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        # 建立连接
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            # 查询所有用户数据
            select_users_query = "SELECT * FROM users ORDER BY created_at DESC LIMIT 10"
            cursor.execute(select_users_query)
            users = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'users': users
            })
    except Exception as e:
        print("数据库操作失败:", str(e))
        return jsonify({
            'success': False,
            'message': f'数据库操作失败: {str(e)}'
        }), 500
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)