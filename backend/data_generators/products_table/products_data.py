import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker('en_US')

def generate_product_name(subcategory_name):
    """Generate a product name related to the subcategory."""
    
    if "Smartphones" in subcategory_name:
        brands = ["iPhone", "Samsung Galaxy", "Google Pixel", "OnePlus", "Xiaomi", "Huawei", "Sony Xperia", "LG", "Motorola", "Nokia"]
        models = [str(random.randint(10, 25)) for _ in range(10)] + ["Pro", "Ultra", "Plus", "Max", "Mini"]
        colors = ["Black", "White", "Blue", "Red", "Green", "Gold", "Silver", "Purple"]
        return f"{random.choice(brands)} {random.choice(models)} {random.choice(colors)}"
    elif "Laptops" in subcategory_name:
        brands = ["MacBook", "Dell XPS", "HP Spectre", "Lenovo ThinkPad", "Asus ROG", "Microsoft Surface", "Acer", "MSI", "Razer", "Samsung"]
        sizes = ["13\"", "14\"", "15\"", "16\"", "17\""]
        types = ["Pro", "Air", "Book", "Laptop", "Notebook"]
        return f"{random.choice(brands)} {random.choice(sizes)} {random.choice(types)}"
    elif "Clothing" in subcategory_name or "Wear" in subcategory_name:
        types = ["T-Shirt", "Jeans", "Dress", "Jacket", "Sweater", "Pants", "Shirt", "Skirt", "Hoodie", "Shorts"]
        materials = ["Cotton", "Denim", "Wool", "Silk", "Polyester", "Linen", "Leather", "Nylon"]
        styles = ["Slim", "Regular", "Oversized", "Vintage", "Modern", "Classic"]
        return f"{random.choice(styles)} {random.choice(materials)} {random.choice(types)}"
    elif "Books" in subcategory_name:
        topics = ["Programming", "History", "Science", "Fiction", "Biography", "Cooking", "Travel", "Health", "Business", "Art"]
        formats = ["Hardcover", "Paperback", "eBook", "Audiobook"]
        return f"The Art of {random.choice(topics)} {random.choice(formats)}"
    elif "Sports" in subcategory_name:
        items = ["Running Shoes", "Yoga Mat", "Dumbbells", "Treadmill", "Basketball", "Tennis Racket", "Soccer Ball", "Bike", "Swim Goggles", "Golf Clubs"]
        brands = ["Nike", "Adidas", "Puma", "Under Armour", "Reebok", "New Balance", "Asics", "Wilson", "Spalding", "Speedo"]
        return f"{random.choice(brands)} {random.choice(items)}"
    elif "Home" in subcategory_name or "Furniture" in subcategory_name:
        items = ["Sofa", "Dining Table", "Chair", "Bed Frame", "Lamp", "Rug", "Cabinet", "Bookshelf", "Desk", "Ottoman"]
        styles = ["Modern", "Classic", "Rustic", "Industrial", "Minimalist", "Traditional", "Scandinavian", "Bohemian"]
        materials = ["Wood", "Metal", "Fabric", "Leather", "Glass", "Plastic"]
        return f"{random.choice(styles)} {random.choice(materials)} {random.choice(items)}"
    elif "Beauty" in subcategory_name:
        products = ["Lipstick", "Foundation", "Shampoo", "Moisturizer", "Perfume", "Nail Polish", "Mascara", "Blush", "Eyeshadow", "Serum"]
        brands = ["MAC", "Maybelline", "L'Oreal", "Estee Lauder", "Clinique", "NARS", "Fenty Beauty", "The Ordinary", "Kiehl's", "Bobbi Brown"]
        return f"{random.choice(brands)} {random.choice(products)}"
    elif "Toys" in subcategory_name:
        toys = ["Action Figure", "Building Blocks", "Puzzle", "Stuffed Animal", "Board Game", "Remote Car", "Doll", "Lego Set", "Bike", "Art Supplies"]
        themes = ["Superhero", "Princess", "Animal", "Space", "Educational", "Adventure", "Fantasy", "Sports", "Music", "Science"]
        return f"{random.choice(themes)} {random.choice(toys)}"
    elif "Automotive" in subcategory_name:
        parts = ["Brake Pads", "Oil Filter", "Tires", "Battery", "Spark Plugs", "Air Filter", "Wipers", "Belts", "Filters", "Lights"]
        brands = ["Bosch", "Michelin", "ACDelco", "Denso", "NGK", "Fram", "Mobil", "Castrol", "Goodyear", "Continental"]
        return f"{random.choice(brands)} {random.choice(parts)}"
    elif "Garden" in subcategory_name:
        garden_items = ["Garden Hose", "Lawn Mower", "Flower Pot", "Garden Tools Set", "Bird Feeder", "Grill", "Patio Furniture", "Seeds", "Fertilizer", "Compost"]
        brands = ["Weber", "Toro", "Black & Decker", "Sun Joe", "Greenworks", " Scotts", "Ortho", "Miracle-Gro", "Burpee", "Rachael Ray"]
        return f"{random.choice(brands)} {random.choice(garden_items)}"
    elif "Food" in subcategory_name:
        foods = ["Organic Apples", "Artisan Bread", "Gourmet Cheese", "Premium Coffee", "Fresh Pasta", "Chocolate Bar", "Wine Bottle", "Tea Set", "Spice Mix", "Honey"]
        origins = ["Italian", "French", "Mexican", "Japanese", "Indian", "Greek", "Spanish", "Thai", "American", "German"]
        return f"{random.choice(origins)} {random.choice(foods)}"
    else:
        # Fallback to more unique generation
        adjectives = ["Advanced", "Premium", "Deluxe", "Essential", "Professional", "Compact", "Heavy-Duty", "Lightweight", "Durable", "Eco-Friendly"]
        nouns = ["Tool", "Device", "System", "Kit", "Set", "Unit", "Module", "Component", "Accessory", "Gadget"]
        return f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(1000, 9999)}"

def generate_related_description(product_name, subcategory_name):
    """Generate a description related to the product and subcategory."""
    base_desc = fake.paragraph(nb_sentences=2)
    
    # Add relevant details based on subcategory
    if "Electronics" in subcategory_name:
        return base_desc + " Featuring cutting-edge technology and sleek design."
    elif "Clothing" in subcategory_name:
        return base_desc + " Made with high-quality materials for comfort and style."
    elif "Books" in subcategory_name:
        return base_desc + " An engaging read that expands your knowledge."
    elif "Sports" in subcategory_name:
        return base_desc + " Perfect for athletes and fitness enthusiasts."
    elif "Home" in subcategory_name:
        return base_desc + " Enhance your living space with this quality item."
    elif "Beauty" in subcategory_name:
        return base_desc + " Professional-grade products for your beauty routine."
    elif "Toys" in subcategory_name:
        return base_desc + " Fun and educational entertainment for children."
    elif "Automotive" in subcategory_name:
        return base_desc + " Reliable parts for optimal vehicle performance."
    elif "Garden" in subcategory_name:
        return base_desc + " Create a beautiful outdoor environment."
    elif "Food" in subcategory_name:
        return base_desc + " Delicious and nutritious culinary delights."
    else:
        return base_desc + f" A premium {subcategory_name.lower()} product."

def get_random_with_error(real_value, error_rate=0.05, error_generator=None):
    """Return real value or error based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return f"Invalid Product {random.randint(1, 1000)}"
    else:
        return real_value

def generate_products_data(subcategory):
    # Error generators
    def invalid_name():
        return "Invalid Product " + str(random.randint(1, 1000))

    def invalid_description():
        return "Invalid description " + str(random.randint(1, 1000))

    create_time = datetime.now()
    delete_time = create_time + timedelta(days=random.randint(1, 365))

    product_id = f"product_id-{uuid.uuid4()}"
    
    # Generate name related to subcategory
    real_name = generate_product_name(subcategory["name"])
    name = get_random_with_error(real_name, error_generator=invalid_name)
    
    # Generate description related to product and subcategory
    if not name.startswith("Invalid"):
        real_desc = generate_related_description(name, subcategory["name"])
        description = get_random_with_error(real_desc, error_generator=invalid_description)
    else:
        description = invalid_description()

    products_data = {
        "id": product_id,
        "name": name,
        "description": description,
        "category_id": subcategory["id"],  # Note: this might be subcategory_id in schema
        "create_time": create_time,
        "delete_time": delete_time
    }
    return products_data