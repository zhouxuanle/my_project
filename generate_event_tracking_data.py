import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from faker_commerce import Provider as CommerceProvider

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

def generate_shipping_status_event(order_id):
    """Generates a fake shipping status update for a given order ID."""
    shipping_statuses = ['shipped', 'in_transit', 'out_for_delivery', 'delivered']
    
    # Use the same order_id to link the events
    event = {
        'event_type': 'shipping_status_update',
        'event_timestamp': (datetime.now() + timedelta(hours=random.randint(1, 48))).isoformat(),
        'order_id': order_id,
        'tracking_number': fake.unique.bothify(text='??#####-##', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'carrier': fake.company(),
        'status': random.choice(shipping_statuses),
        'estimated_delivery': (datetime.now() + timedelta(days=random.randint(2, 7))).isoformat()
    }
    return event


# Number of records to generate
NUM_CATEGORIES = 10
NUM_SUBCATEGORIES_PER_CATEGORY = 5
NUM_PRODUCTS_PER_SUBCATEGORY = 10

# Store generated data to maintain relationships
categories_data = []
subcategories_data = []
products_data = []

# 1. Generate Categories Table Data
for _ in range(NUM_CATEGORIES):
    category_id = str(uuid.uuid4())
    category_name = fake.unique.word().capitalize() + " Category"
    categories_data.append({
        "category_id": category_id,
        "category_name": category_name
    })

# 2. Generate Subcategories Table Data
for category in categories_data:
    for _ in range(NUM_SUBCATEGORIES_PER_CATEGORY):
        subcategory_id = str(uuid.uuid4())
        subcategory_name = fake.unique.word().capitalize() + " Subcategory"
        subcategories_data.append({
            "subcategory_id": subcategory_id,
            "category_id": category["category_id"],
            "subcategory_name": subcategory_name
        })

# 3. Generate Products Table Data
for subcategory in subcategories_data:
    for _ in range(NUM_PRODUCTS_PER_SUBCATEGORY):
        product_id = str(uuid.uuid4())
        product_name = fake.unique.catch_phrase()
        product_description = fake.paragraph()
        product_price = round(random.uniform(5.0, 500.0), 2)
        product_stock = random.randint(0, 200)
        products_data.append({
            "product_id": product_id,
            "subcategory_id": subcategory["subcategory_id"],
            "product_name": product_name,
            "product_description": product_description,
            "product_price": product_price,
            "product_stock": product_stock
        })

# --- Generate and print the data ---
purchase_event, linked_order_id = generate_online_purchase_event()
shipping_event = generate_shipping_status_event(linked_order_id)

print("--- Online Purchase Event ---")
print(purchase_event)

print("\n--- Shipping Status Update Event ---")
print(shipping_event)
