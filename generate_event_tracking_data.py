import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from faker_commerce import Provider as CommerceProvider
from random import randint

# Initialize Faker with a locale
fake = Faker('en_US')

# Add the commerce provider to the faker instance
fake.add_provider(CommerceProvider)

# Generate user_info Table Data
def generate_user_data():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    profile = fake.profile()
    age = fake.random_int(min=18, max=90) 
    user_id = f"user_id-{uuid.uuid4()}"
    password_default = fake.password()
    user_info_data = {
        "id": user_id,
        "username": profile['username'],
        "real_name": profile['name'],
        "phone_number": fake.phone_number(),
        "sex": profile['sex'],
        "job": profile['job'],
        "company": profile['company'],
        "email": profile['mail'],
        "password":password_default,
        "birth_of_date": profile['birthdate'],
        "age": age,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return user_info_data

# Generate Address Table Data
def generate_fake_address(user):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    address_titles = [
        "Home Address",
        "Work Address",
        "Billing Address",
        "Shipping Address",
        "Vacation Home"
    ]
    street_address = fake.street_address()
    secondary_address = fake.secondary_address()
    full_address_line = f"{street_address} {secondary_address}"
    address_id = f"address_id-{uuid.uuid4()}"
    address_data = {
        "id": address_id,
        "user_id":user["id"],
        "title": random.choice(address_titles),
        "address_line": full_address_line,
        "country": fake.country(),
        "city": fake.city(),
        "postal_code": fake.postcode(),
        "create_time": create_time,
        "delete_time": delete_time
    }
    
    return address_data


# Generate Categories Table Data
def generate_categories_data():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    category_id = f"category_id-{uuid.uuid4()}"
    category_name = fake.ecommerce_category()
    description = fake.text(max_nb_chars=10)
    categories_data = {
        "id": category_id, 
        "name": category_name,
        "description": description,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return categories_data

# Generate Subcategories Table Data
def generate_subcategories_data(category):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    subcategory_id = f"subcategory_id-{uuid.uuid4()}"
    subcategory_name = fake.unique.word().capitalize() + " Subcategory"
    description = fake.text(max_nb_chars=50)
    subcategories_data = {
        "id": subcategory_id,
        "parent_id": category["id"],
        "name": subcategory_name,
        "description": description,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return subcategories_data

# Generate Products Table Data
def generate_products_data(subcategory):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    product_id = f"product_id-{uuid.uuid4()}"
    product_name = fake.unique.catch_phrase()
    product_description = fake.paragraph()  
    products_data = {
        "id": product_id,
        "name": product_name,
        "description": product_description,
        "category_id": subcategory["id"],  
        "create_time": create_time,
        "delete_time": delete_time
    }
    return products_data

# Generate product_sku Table Data
def generate_sku_data(category,subcategory,product):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    sku_id = f"sku_id-{uuid.uuid4()}"
    sku_number = fake.unique.random_number(digits=5, fix_len=True)
    sku = f"{category['id'][-3:]}-{subcategory['id'][-3:]}-{product['id'][-3:]}-{sku_id[-3:]}"
    price = round(random.uniform(5.0, 500.0), 2)  
    quantity = random.randint(0, 1000)          
    
    skus_data = {
        "id": sku_id,
        "product_id": product["id"],
        "sku": sku,
        "price": price,
        "quantity": quantity,
        "create_time": create_time,
        "delete_time": delete_time
        }

    return skus_data

# Generate Wishlist Table Data
def generate_wishlist_data(product,user):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    wishlist_id = f"wishlist_id-{uuid.uuid4()}"
    wishlists_data = {
        'id': wishlist_id,
        'user_id': user["id"],
        'product_id': product["id"],
        "create_time": create_time,
        "delete_time": delete_time
            }
    return wishlists_data

# Generate Cart Table Data
def generate_cart_data(user,products_sku,cartItem):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    cart_id = f"cart_id-{uuid.uuid4()}"
    total_price = cartItem["quantity"] * products_sku["price"]
    carts_data = {
        'id': cart_id,
        'user_id': user["id"],
        'total':total_price,
        "create_time": create_time,
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now')
        }
    return carts_data

# Generate CartItem Table Data
def generate_cartItem_data(cart,product,products_sku):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    cartItem_id = f"cartItem_id-{uuid.uuid4()}"
    cart_items_data = {
        'id': cartItem_id,
        'cart_id': cart["id"],
        'product_id': product["id"],
        'products_sku_id': products_sku["id"],
        'quantity': random.randint(1, 5),
        "create_time": create_time,
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now')
        }
    return cart_items_data

# Generate Order_details Table Data
def generate_Order_details_data(order_item,user,products_sku):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    order_details_id = f"order_details_id-{uuid.uuid4()}"
    order_details_data = {
        'id': order_details_id,
        'user_id': user["id"],
        'payment_id':0,
        'total': order_item["quantity"] * products_sku["price"],
        "create_time": create_time,
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now')
        }
    return order_details_data


# Generate Order_item Table Data
def generate_Order_item_data(product,products_sku,order):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    order_item_id = f"order_item_id-{uuid.uuid4()}"
    order_item_data = {
        'id': order_item_id,
        'order_id': order["id"],
        'product_id': product["id"],
        'products_sku_id': products_sku["id"],
        'quantity': random.randint(1, 99999999),
        "create_time": create_time,
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now')
        }
    return order_item_data


# Generate Payment_details Table Data
def generate_Payment_details_data(order_details):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    payment_details_id = f"payment_details_id-{uuid.uuid4()}"
    payment_statuses = ['Success', 'Pending', 'Failed', 'Refunded']
    if order_details[''] is None:
        payment_amount = 0
    else:
        payment_amount = order_details['total']
    payment_details_data = {
        'id': payment_details_id,
        'order_details_id': order_details["id"],
        'amount': payment_amount,
        'provider':fake.credit_card_full().split('\n')[0].strip(),
        'status':random.choice(payment_statuses) ,
        "create_time": create_time,
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now')
        }
    return payment_details_data  




    
print('sss')