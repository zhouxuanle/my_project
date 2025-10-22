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
        
        with connection.cursor() as cursor:
 
            # 插入用户数据到数据库
            insert_query = """
            INSERT INTO users (id, user_name, real_name, phone_number, sex, job, company, email, password, birth_of_date, age, created_at, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
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
            
            # 提交事务
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': f'用户:{user["real_name"]}',
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

if __name__ == '__main__':
    app.run(debug=True)