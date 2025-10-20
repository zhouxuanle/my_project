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


class DataGenerator:
    def __init__(self):
        self.create_time = fake.date_time_between(start_date = '-2y', end_date = 'now')
        self.delete_time = fake.date_time_between(start_date = self.create_time, end_date = 'now')
        self.update_time = fake.date_time_between(start_date = self.create_time, end_date = self.delete_time)

    # Generate user_info Table Data
    def generate_user_data(self):
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
            "create_time": self.create_time,
            "delete_time": self.delete_time
        }
        return user_info_data

    # Generate Address Table Data
    def generate_fake_address(self,user):
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
            "create_time": self.create_time,
            "delete_time": self.delete_time
        }
        
        return address_data


    # Generate Categories Table Data
    def generate_categories_data(self):
        category_id = f"category_id-{uuid.uuid4()}"
        category_name = fake.ecommerce_category()
        description = fake.text(max_nb_chars=10)
        categories_data = {
            "id": category_id, 
            "name": category_name,
            "description": description,
            "create_time": self.create_time,
            "delete_time": self.delete_time
        }
        return categories_data

    # Generate Subcategories Table Data
    def generate_subcategories_data(self,category):
        subcategory_id = f"subcategory_id-{uuid.uuid4()}"
        subcategory_name = fake.unique.word().capitalize() + " Subcategory"
        description = fake.text(max_nb_chars=50)
        subcategories_data = {
            "id": subcategory_id,
            "parent_id": category["id"],
            "name": subcategory_name,
            "description": description,
            "create_time": self.create_time,
            "delete_time": self.delete_time
        }
        return subcategories_data

    # Generate Products Table Data
    def generate_products_data(self,subcategory):
        product_id = f"product_id-{uuid.uuid4()}"
        product_name = fake.unique.catch_phrase()
        product_description = fake.paragraph()  
        products_data = {
            "id": product_id,
            "name": product_name,
            "description": product_description,
            "category_id": subcategory["id"],  
            "create_time": self.create_time,
            "delete_time": self.delete_time
        }
        return products_data

    # Generate product_sku Table Data
    def generate_sku_data(self,category,subcategory,product):
        sku_number = fake.unique.random_number(digits=5, fix_len=True)
        sku_id = f"{category['id'][-3:]}-{subcategory['id'][-3:]}-{product['id'][-3:]}-{sku_number}"
        price = round(random.uniform(5.0, 500.0), 2)  
        stock = random.randint(0, 9999999)          
        
        skus_data = {
            "id": sku_id,
            "product_id": product["id"],
            "price": price,
            "quantity": stock,
            "create_time": self.create_time,
            "delete_time": self.delete_time
            }

        return skus_data

    # Generate Wishlist Table Data
    def generate_wishlist_data(self,products_sku,user):
        wishlist_id = f"wishlist_id-{uuid.uuid4()}"
        wishlists_data = {
            'id': wishlist_id,
            'user_id': user["id"],
            'products_sku_id': products_sku["id"],
            "create_time": self.create_time,
            "delete_time": self.delete_time
                }
        return wishlists_data

    # Generate Cart Table Data
    def generate_cart_data(self,products_sku,order):
        cart_id = f"cart_id-{uuid.uuid4()}"
        quantity = random.randint(1, 9999)
        carts_data = {
            'id': cart_id,
            'order_id': order["id"],
            'products_sku_id': products_sku["id"],
            'quantity' : quantity,
            "create_time": self.create_time,
            'updated_at': self.update_time
            }
        return carts_data

    # Generate Order_details Table Data
    def generate_order_details_data(self,user,payment):
        create_time = fake.date_time_between(start_date='-2y', end_date='now')
        order_details_id = f"order_details_id-{uuid.uuid4()}"
        order_details_data = {
            'id': order_details_id,
            'user_id': user["id"],
            'payment_id':payment["id"],
            "create_time": self.create_time,
            'updated_at': self.update_time
            }
        return order_details_data


    # Generate Order_item Table Data
    def generate_order_item_data(self,products_sku,order):
        create_time = fake.date_time_between(start_date='-2y', end_date='now')
        order_item_id = f"order_item_id-{uuid.uuid4()}"
        order_item_data = {
            'id': order_item_id,
            'order_id': order["id"],
            'products_sku_id': products_sku["id"],
            'quantity': random.randint(1, 99999999),
            "create_time": self.create_time,
            'updated_at': self.update_time
            }
        return order_item_data


    # Generate Payment_details Table Data
    def generate_payment_details_data(self):
        create_time = fake.date_time_between(start_date='-2y', end_date='now')
        payment_details_id = f"payment_details_id-{uuid.uuid4()}"
        payment_statuses = ['Success', 'Pending', 'Failed', 'Refunded']
        payment_details_data = {
            'id': payment_details_id,
            #这里后面通过spark计算，写入这个字段里
            'amount': 0,
            'provider':fake.credit_card_full().split('\n')[0].strip(),
            'status':random.choice(payment_statuses) ,
            "create_time": self.create_time,
            'updated_at': self.update_time
            }
        return payment_details_data  




