import random
from datetime import datetime, timedelta
import uuid

def get_random_with_error(real_value, error_rate=0.05, error_generator=None):
    """Return real value or error based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return f"Invalid {real_value[:10]} " + str(random.randint(1, 1000))
    else:
        return real_value

def generate_wishlist_data(products_sku, user):
    # Error generators
    def invalid_user_id():
        return f"invalid-user-{random.randint(1, 1000)}"

    def invalid_sku_id():
        return f"invalid-sku-{random.randint(1, 1000)}"

    create_time = datetime.now()
    delete_time = create_time + timedelta(days=random.randint(1, 365))

    wishlist_id = f"wishlist_id-{uuid.uuid4()}"
    
    # Generate with possible errors
    user_id = get_random_with_error(user["id"], error_generator=invalid_user_id)
    products_sku_id = get_random_with_error(products_sku["id"], error_generator=invalid_sku_id)

    wishlist_data = {
        "id": wishlist_id,
        "user_id": user_id,
        "products_sku_id": products_sku_id,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return wishlist_data