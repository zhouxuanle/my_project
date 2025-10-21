from generate_event_tracking_data import DataGenerator 
 
gd = DataGenerator()
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

data_li = [user,address,category,subcategory,product,products_sku,wishlist,payment,order,order_item,cart]

count = 1
for i in data_li:
    # print(count)
    # print(i,end="\n")
    count += 1


###################


import pymysql

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

try:
    # 建立连接
    connection = pymysql.connect(**config)
    
    with connection.cursor() as cursor:
        # 执行一个简单的查询
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print("MySQL 版本:", result)

except Exception as e:
    print("数据库连接失败:", str(e))
finally:
    if 'connection' in locals():
        connection.close()


