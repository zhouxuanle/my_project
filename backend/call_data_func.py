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





