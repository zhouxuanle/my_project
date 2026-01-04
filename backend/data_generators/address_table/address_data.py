import random
from datetime import datetime, timedelta
import uuid
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load data from files
with open(os.path.join(script_dir, 'data', 'address_lines.txt'), 'r', encoding='utf-8') as f:
    address_lines = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'postal_codes.txt'), 'r', encoding='utf-8') as f:
    postal_codes = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'cities.txt'), 'r', encoding='utf-8') as f:
    cities = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'countries.txt'), 'r', encoding='utf-8') as f:
    countries = [line.strip() for line in f]

address_titles = [
    "Home Address",
    "Work Address",
    "Billing Address",
    "Shipping Address",
    "Vacation Home"
]

def get_random_with_error(real_data, error_rate=0.3, error_generator=None):
    """Return real data or error data based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return None  # Or some default error
    else:
        return random.choice(real_data)

def generate_fake_address(user):
    # Error generators
    def invalid_address_line():
        return "Invalid Address " + str(random.randint(1, 1000))

    def invalid_postal_code():
        return "INVALID" + str(random.randint(100, 999))

    def invalid_city():
        return "InvalidCity" + str(random.randint(1, 1000))

    def invalid_country():
        return "Invalid Country " + str(random.randint(1, 100))

    def invalid_title():
        return "Invalid Title " + str(random.randint(1, 10))

    create_time = datetime.now()
    delete_time = create_time + timedelta(days=random.randint(1, 365))

    address_id = f"address_id-{uuid.uuid4()}"
    title = get_random_with_error(address_titles, error_generator=invalid_title)
    address_line = get_random_with_error(address_lines, error_generator=invalid_address_line)
    # Pick matching country and city
    index = random.randint(0, len(countries)-1)
    country = countries[index]
    city = cities[index]
    postal_code = get_random_with_error(postal_codes, error_generator=invalid_postal_code)

    address_data = {
        "id": address_id,
        "user_id": user["id"],
        "title": title,
        "address_line": address_line,
        "country": country,
        "city": city,
        "postal_code": postal_code,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return address_data