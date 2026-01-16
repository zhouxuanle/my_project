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

def generate_order_details_data(user, payment):
    # Error generators
    def invalid_user_id():
        return f"invalid-user-{random.randint(1, 1000)}"

    def invalid_payment_id():
        return f"invalid-payment-{random.randint(1, 1000)}"

    create_time = datetime.now()
    update_time = create_time + timedelta(days=random.randint(0, 30))  # Shorter update window

    order_details_id = f"order_details_id-{uuid.uuid4()}"
    
    # Generate with possible errors
    user_id = get_random_with_error(user["id"], error_generator=invalid_user_id)
    payment_id = get_random_with_error(payment["id"], error_generator=invalid_payment_id)

    order_details_data = {
        'id': order_details_id,
        'user_id': user_id,
        'payment_id': payment_id,
        "create_time": create_time,
        'updated_at': update_time
    }
    return order_details_data