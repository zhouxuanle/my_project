import random
from datetime import datetime, timedelta
import uuid
import os
from faker import Faker

fake = Faker('en_US')

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load data from files
with open(os.path.join(script_dir, 'data', 'category_names.txt'), 'r') as f:
    category_names = [line.strip() for line in f]

def generate_related_description(category_name):
    """Generate a description related to the category name."""
    if "Electronics" in category_name:
        return fake.sentence(nb_words=5) + " Perfect for tech enthusiasts."
    elif "Clothing" in category_name:
        return fake.sentence(nb_words=5) + " Stylish and comfortable wear."
    elif "Home" in category_name:
        return fake.sentence(nb_words=5) + " Essential for modern living."
    elif "Books" in category_name:
        return fake.sentence(nb_words=5) + " Expand your knowledge."
    elif "Sports" in category_name:
        return fake.sentence(nb_words=5) + " For active lifestyles."
    elif "Beauty" in category_name:
        return fake.sentence(nb_words=5) + " Enhance your natural beauty."
    elif "Toys" in category_name:
        return fake.sentence(nb_words=5) + " Fun for all ages."
    elif "Automotive" in category_name:
        return fake.sentence(nb_words=5) + " Keep your vehicle running smoothly."
    elif "Garden" in category_name:
        return fake.sentence(nb_words=5) + " Beautify your outdoor space."
    elif "Food" in category_name:
        return fake.sentence(nb_words=5) + " Delicious and nutritious options."
    else:
        return fake.sentence(nb_words=5) + f" High-quality {category_name.lower()} products."

def get_random_with_error(real_data, error_rate=0.3, error_generator=None):
    """Return real data or error data based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return None
    else:
        return random.choice(real_data)

def generate_categories_data():
    # Error generators
    def invalid_name():
        return "Invalid Category " + str(random.randint(1, 1000))

    def invalid_description():
        return "Invalid description " + str(random.randint(1, 1000))

    create_time = datetime.now()
    delete_time = create_time + timedelta(days=random.randint(1, 365))

    category_id = f"category_id-{uuid.uuid4()}"
    name = get_random_with_error(category_names, error_generator=invalid_name)
    
    if name and not name.startswith("Invalid"):
        description = generate_related_description(name)
        # Apply error to description
        if random.random() < 0.3:
            description = invalid_description()
    else:
        description = invalid_description()

    categories_data = {
        "id": category_id,
        "name": name,
        "description": description,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return categories_data