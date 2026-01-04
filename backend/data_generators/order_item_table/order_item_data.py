import random
from datetime import datetime, timedelta
import uuid

def get_random_with_error(real_value, error_rate=0.3, error_generator=None):
    """Return real value or error based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return f"Invalid {type(real_value).__name__} " + str(random.randint(1, 1000))
    else:
        return real_value

def generate_order_item_data(products_sku, order):
    # Error generators
    def invalid_order_id():
        return f"invalid-order-{random.randint(1, 1000)}"

    def invalid_sku_id():
        return f"invalid-sku-{random.randint(1, 1000)}"

    def invalid_quantity():
        return random.choice([-50, "invalid", None, 999999999])

    create_time = datetime.now()
    update_time = create_time + timedelta(days=random.randint(0, 30))

    order_item_id = f"order_item_id-{uuid.uuid4()}"
    
    # Generate with possible errors
    order_id = get_random_with_error(order["id"], error_generator=invalid_order_id)
    products_sku_id = get_random_with_error(products_sku["id"], error_generator=invalid_sku_id)
    quantity = get_random_with_error(random.randint(1, 99999999), error_generator=invalid_quantity)

    order_item_data = {
        'id': order_item_id,
        'order_id': order_id,
        'products_sku_id': products_sku_id,
        'quantity': quantity,
        "create_time": create_time,
        'updated_at': update_time
    }
    return order_item_data