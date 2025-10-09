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
def generate_fake_address():
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    # Custom titles for the address, since Faker doesn't have a specific provider for this.
    address_titles = [
        "Home Address",
        "Work Address",
        "Billing Address",
        "Shipping Address",
        "Vacation Home"
    ]
    
        # Combine address parts from Faker
    street_address = fake.street_address()
    secondary_address = fake.secondary_address()
    full_address_line = f"{street_address} {secondary_address}"

    address_data = {
        "id": str(uuid.uuid4()),
        "user_id":""
        "title": choice(address_titles),
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
    category_id = str(uuid.uuid4())  
    category_name = fake.ecommerce_category()
    description = fake.text(max_nb_chars=10)
    categories_data = {
        "id": category_id, 
        "category_name": category_name,
        "description": description,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return categories_data

# Generate Subcategories Table Data
def generate_subcategories_data(category):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    subcategory_id = str(uuid.uuid4())
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
    product_id = str(uuid.uuid4())
    product_name = fake.unique.catch_phrase()
    product_description = fake.paragraph()
    # product_price = round(random.uniform(5.0, 500.0), 2)
    # product_stock = random.randint(0, 200)
    products_data = {
        "id": product_id,
        "name": product_name,
        "description": product_description,
        "subcategory_id": subcategory["id"],
        # "product_price": product_price,
        # "product_stock": product_stock,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return products_data

# Generate product_sku Table Data
def generate_sku_data(product):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    sku_id = fake.unique.random_int(min=1, max=num_rows * 10)
    brand = fake.word().upper()
    product_type = fake.word().upper()
    sku_number = fake.unique.random_number(digits=5, fix_len=True)
    sku = f"{brand[:3]}-{product_type[:3]}-{sku_number}"
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
def generate_cart_data_event(user,products_sku,cartItem):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    cart_id = fake.unique.random_int(min=1, max=99999999999)
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
def generate_cartItem_data_event(cart,product,products_sku):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    cartItem_id = fake.unique.random_int(min=1, max=99999999999)
    cart_items_data = {
        'id': cartItem_id,
        'cart_id': cart["id"],
        'product_id': products_sku["id"],
        'quantity': random.randint(1, 5),
        "create_time": create_time,
        'updated_at': fake.date_time_between(start_date='-6m', end_date='now')
        }
    return cart_items_data

# Generate Wishlist Table Data
def generate_wishlist_data(product,user):
    create_time = fake.date_time_between(start_date='-2y', end_date='now')
    delete_time = fake.date_time_between(start_date=create_time, end_date='now')
    wishlist_id = fake.unique.random_int(min=1, max=99999999999)
    wishlists_data = {
        'id': wishlist_id,
        'user_id': user["id"],
        'product_id': product["id"],
        "create_time": create_time,
        "delete_time": delete_time
            }
    return wishlists_data
    
print('sss')