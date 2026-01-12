import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker('en_US')

def generate_subcategory_name(category_name):
    """Generate a subcategory name related to the category."""
    if "Electronics" in category_name:
        prefixes = ["Smartphones", "Laptops", "Tablets", "Accessories", "Audio", "Gaming", "Wearables", "Cameras"]
    elif "Clothing" in category_name:
        prefixes = ["Men's Wear", "Women's Wear", "Kids' Clothing", "Shoes", "Accessories", "Sportswear", "Formal", "Casual"]
    elif "Home" in category_name:
        prefixes = ["Furniture", "Decor", "Kitchen", "Bathroom", "Bedding", "Lighting", "Storage", "Appliances"]
    elif "Books" in category_name:
        prefixes = ["Fiction", "Non-Fiction", "Textbooks", "Children's Books", "Biographies", "Science", "History", "Self-Help"]
    elif "Sports" in category_name:
        prefixes = ["Fitness", "Outdoor", "Team Sports", "Water Sports", "Winter Sports", "Equipment", "Apparel", "Footwear"]
    elif "Beauty" in category_name:
        prefixes = ["Skincare", "Makeup", "Hair Care", "Fragrance", "Nails", "Tools", "Men's Grooming", "Wellness"]
    elif "Toys" in category_name:
        prefixes = ["Action Figures", "Dolls", "Educational", "Outdoor", "Building", "Puzzles", "Board Games", "Ride-On"]
    elif "Automotive" in category_name:
        prefixes = ["Parts", "Accessories", "Tools", "Electronics", "Interior", "Exterior", "Maintenance", "Safety"]
    elif "Garden" in category_name:
        prefixes = ["Plants", "Tools", "Furniture", "Decor", "Pots", "Seeds", "Irrigation", "Pest Control"]
    elif "Food" in category_name:
        prefixes = ["Snacks", "Beverages", "Organic", "Bakery", "Dairy", "Meat", "Produce", "Pantry"]
    else:
        prefixes = ["Basic", "Advanced", "Premium", "Essential", "Specialty", "Standard", "Deluxe", "Compact"]
    
    prefix = random.choice(prefixes)
    cleaned_category = category_name.replace('Home & ', '').replace('Outdoor ', '').replace('Professional ', '').replace("Kids' ", '').replace('Luxury ', '').replace('Budget ', '').replace('Eco-Friendly ', '').replace('Smart ', '').replace('Vintage ', '')
    return f"{prefix} {cleaned_category}"

def generate_related_description(subcategory_name, category_name):
    """Generate a description related to the subcategory and category."""
    base_desc = fake.sentence(nb_words=6)
    if "Electronics" in category_name:
        return base_desc + " Cutting-edge technology for modern needs."
    elif "Clothing" in category_name:
        return base_desc + " Stylish and comfortable fashion choices."
    elif "Home" in category_name:
        return base_desc + " Enhance your living space."
    elif "Books" in category_name:
        return base_desc + " Expand your knowledge and imagination."
    elif "Sports" in category_name:
        return base_desc + " Gear up for an active lifestyle."
    elif "Beauty" in category_name:
        return base_desc + " Pamper yourself with quality products."
    elif "Toys" in category_name:
        return base_desc + " Fun and educational entertainment."
    elif "Automotive" in category_name:
        return base_desc + " Keep your vehicle in top condition."
    elif "Garden" in category_name:
        return base_desc + " Cultivate a beautiful outdoor environment."
    elif "Food" in category_name:
        return base_desc + " Delicious and nutritious options."
    else:
        return base_desc + f" Quality {category_name.lower()} products."

def get_random_with_error(real_value, error_rate=0.3, error_generator=None):
    """Return real value or error based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return f"Invalid {real_value[:10]} " + str(random.randint(1, 1000))
    else:
        return real_value

def generate_subcategories_data(category):
    # Error generators
    def invalid_name():
        return "Invalid Subcategory " + str(random.randint(1, 1000))

    def invalid_description():
        return "Invalid description " + str(random.randint(1, 1000))

    create_time = datetime.now()
    delete_time = create_time + timedelta(days=random.randint(1, 365))

    subcategory_id = f"subcategory_id-{uuid.uuid4()}"
    
    # Generate name related to category
    real_name = generate_subcategory_name(category["name"])
    name = get_random_with_error(real_name, error_generator=invalid_name)
    
    # Generate description related to subcategory and category
    if not name.startswith("Invalid"):
        real_desc = generate_related_description(name, category["name"])
        description = get_random_with_error(real_desc, error_generator=invalid_description)
    else:
        description = invalid_description()

    subcategories_data = {
        "id": subcategory_id,
        "parent_id": category["id"],
        "name": name,
        "description": description,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return subcategories_data