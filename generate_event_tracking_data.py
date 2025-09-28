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

def generate_online_purchase_event():
    """Generates a fake online shopping event."""
    order_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    # Generate a list of random products
    products = []
    num_products = random.randint(1, 50)
    for _ in range(num_products):
        products.append({
            'product_id': str(uuid.uuid4()),
            'product_name': fake.ecommerce_name(),
            'price': round(random.uniform(5.0, 500.0), 2),
            'quantity': random.randint(1, 5)
        })
        
    # Calculate the total purchase amount
    total_amount = sum(item['price'] * item['quantity'] for item in products)

    event = {
        'event_type': 'online_purchase',
        'event_timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'order_id': order_id,
        'payment_method': fake.credit_card_provider(),
        'shipping_address': {
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'country': fake.country()
        },
        'products': products,
        'total_amount': round(total_amount, 2)
    }
    return event, order_id




# Generate user_info Table Data
def generate_user_data():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    profile = fake.profile()
    age = fake.random_int(min=18, max=90)
    user_id = str(uuid.uuid4())
    user_info_data = {
        "user_id": user_id,
        "username": profile['username'],
        "name": profile['name'],
        "phone_number": fake.phone_number(),
        "sex": profile['sex'],
        "job": profile['job'],
        "company": profile['company'],
        "address": profile['address'],
        "mail": profile['mail'],
        "birthdate": profile['birthdate'],
        "age": age,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return user_info_data



# Generate Categories Table Data
def generate_categories_data_event():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    category_id = str(uuid.uuid4())  
    category_name = fake.unique.word().capitalize() + " Category"
    categories_data = {
        "category_id": category_id, 
        "category_name": category_name,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return categories_data

# Generate Subcategories Table Data
def generate_subcategories_data_event(category):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    subcategory_id = str(uuid.uuid4())
    subcategory_name = fake.unique.word().capitalize() + " Subcategory"
    subcategories_data = {
        "subcategory_id": subcategory_id,
        "category_id": category["category_id"],
        "subcategory_name": subcategory_name,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return subcategories_data

# Generate Products Table Data
def generate_products_data_event(subcategory):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    product_id = str(uuid.uuid4())
    product_name = fake.unique.catch_phrase()
    product_description = fake.paragraph()
    product_price = round(random.uniform(5.0, 500.0), 2)
    product_stock = random.randint(0, 200)
    products_data = {
        "product_id": product_id,
        "subcategory_id": subcategory["subcategory_id"],
        "product_name": product_name,
        "product_description": product_description,
        "product_price": product_price,
        "product_stock": product_stock,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return products_data

# Generate shipping Table Data
def generate_shipping_status_event(order_id):
    shipping_statuses = ['shipped', 'in_transit', 'out_for_delivery', 'delivered']
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    shipping_data = {
        'order_id': order_id,
        'tracking_number': fake.unique.bothify(text='??#####-##', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'carrier': fake.company(),
        'status': random.choice(shipping_statuses),
        'estimated_delivery': (datetime.now() + timedelta(days=random.randint(2, 7))).isoformat(),
        "create_time": create_time,
        "delete_time": delete_time
    }
    return shipping_data

# Generate Cart Table Data
def generate_cart_data_event():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    carts_data = {
        'cart_id': i,
        'user_id': random.choice(user_ids),
        'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now'),
        "create_time": create_time,
        "delete_time": delete_time
        }
    return carts_data

# Generate CartItem Table Data
def generate_cartItem_data_event():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    cart_items_data = {
        'cart_item_id': i,
        'cart_id': random.choice(cart_ids),
        'product_id': random.choice(product_ids),
        'quantity': random.randint(1, 5),
        'added_at': fake.date_time_between(start_date='-6m', end_date='now'),
        "create_time": create_time,
        "delete_time": delete_time
        }
    return cart_items_data

# Generate Wishlist Table Data
def generate_wishlist_data_event():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    wishlists_data = {
        'wishlist_id': i,
        'user_id': user_id,
        'product_id': product_id,
        'added_at': fake.date_time_between(start_date='-1y', end_date='now'),
        "create_time": create_time,
        "delete_time": delete_time
            }