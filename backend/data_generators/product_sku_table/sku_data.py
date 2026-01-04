import random
from datetime import datetime, timedelta
import uuid

def get_random_with_error(real_value, error_rate=0.3, error_generator=None):
    """Return real value or error based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return f"Invalid {real_value}"
    else:
        return real_value

def generate_sku_data(category, subcategory, product):
    # Error generators
    def invalid_price():
        return random.choice([-50.0, "invalid", None, 999999.99])

    def invalid_quantity():
        return random.choice([-100, "invalid", None, 99999999])

    create_time = datetime.now()
    delete_time = create_time + timedelta(days=random.randint(1, 365))

    # Generate SKU number (5 digits)
    sku_number = str(random.randint(10000, 99999))
    sku_id = f"{category['id'][-3:]}-{subcategory['id'][-3:]}-{product['id'][-3:]}-{sku_number}"

    # Generate price with possible error
    real_price = round(random.uniform(5.0, 500.0), 2)
    price = get_random_with_error(real_price, error_generator=invalid_price)

    # Generate quantity with possible error
    real_quantity = random.randint(0, 9999999)
    quantity = get_random_with_error(real_quantity, error_generator=invalid_quantity)

    skus_data = {
        "id": sku_id,
        "product_id": product["id"],
        "price": price,
        "quantity": quantity,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return skus_data