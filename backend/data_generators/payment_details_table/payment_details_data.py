import random
from datetime import datetime, timedelta
import uuid
from faker import Faker

fake = Faker('en_US')

payment_statuses = ['Success', 'Pending', 'Failed', 'Refunded']

def get_random_with_error(real_value, error_rate=0.3, error_generator=None):
    """Return real value or error based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return f"Invalid {type(real_value).__name__} " + str(random.randint(1, 1000))
    else:
        return real_value

def generate_payment_details_data():
    # Error generators
    def invalid_amount():
        return random.choice([-100.0, "invalid", None, 9999999.99])

    def invalid_provider():
        return f"Invalid Provider {random.randint(1, 1000)}"

    def invalid_status():
        return f"Invalid Status {random.randint(1, 1000)}"

    create_time = datetime.now()
    update_time = create_time + timedelta(days=random.randint(0, 30))

    payment_details_id = f"payment_details_id-{uuid.uuid4()}"
    
    # Generate with possible errors
    amount = get_random_with_error(0, error_generator=invalid_amount)  # Keep 0 for Spark calculation
    provider = get_random_with_error(fake.credit_card_full().split('\n')[0].strip(), error_generator=invalid_provider)
    status = get_random_with_error(random.choice(payment_statuses), error_generator=invalid_status)

    payment_details_data = {
        'id': payment_details_id,
        'amount': amount,
        'provider': provider,
        'status': status,
        "create_time": create_time,
        'updated_at': update_time
    }
    return payment_details_data