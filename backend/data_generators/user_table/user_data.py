import random
from datetime import datetime, timedelta, date
import uuid
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load data from files
with open(os.path.join(script_dir, 'data', 'usernames.txt'), 'r') as f:
    usernames = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'real_names.txt'), 'r') as f:
    real_names = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'phone_numbers.txt'), 'r') as f:
    phone_numbers = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'emails.txt'), 'r') as f:
    emails = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'passwords.txt'), 'r') as f:
    passwords = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'jobs.txt'), 'r') as f:
    jobs = [line.strip() for line in f]

with open(os.path.join(script_dir, 'data', 'companies.txt'), 'r') as f:
    companies = [line.strip() for line in f]

from datetime import date
with open(os.path.join(script_dir, 'data', 'birth_dates.txt'), 'r') as f:
    birth_dates = [date.fromisoformat(line.strip()) for line in f]

sex_options = ['male', 'female', 'other']

def get_random_with_error(real_data, error_rate=0.05, error_generator=None):
    """Return real data or error data based on error rate."""
    if random.random() < error_rate:
        if error_generator:
            return error_generator()
        else:
            return None  # Or some default error
    else:
        return random.choice(real_data)

def generate_user_data():
    create_time = datetime.now()
    delete_time = datetime.now() + timedelta(days=random.randint(1, 365))

    # Error generators
    def invalid_username():
        return str(random.randint(1000, 9999)) + "@invalid"

    def invalid_real_name():
        return "InvalidName" + str(random.randint(1, 1000))

    def invalid_phone():
        return "invalid-phone-" + str(random.randint(1, 1000))

    def invalid_sex():
        return random.choice(["unknown", "123", ""])

    def invalid_job():
        return "Invalid Job " + str(random.randint(1, 100))

    def invalid_company():
        return "Invalid Company " + str(random.randint(1, 100))

    def invalid_email():
        return "invalid.email" + str(random.randint(1, 1000)) + "@bad"

    def invalid_password():
        return "123"  # Too simple

    def invalid_birth_date():
        # Future date
        return date.today() + timedelta(days=random.randint(1, 365*10))

    user_id = f"user_id-{uuid.uuid4()}"
    username = get_random_with_error(usernames, error_generator=invalid_username)
    real_name = get_random_with_error(real_names, error_generator=invalid_real_name)
    phone_number = get_random_with_error(phone_numbers, error_generator=invalid_phone)
    sex = get_random_with_error(sex_options, error_generator=invalid_sex)
    job = get_random_with_error(jobs, error_generator=invalid_job)
    company = get_random_with_error(companies, error_generator=invalid_company)
    email = get_random_with_error(emails, error_generator=invalid_email)
    password = get_random_with_error(passwords, error_generator=invalid_password)
    birth_of_date = get_random_with_error(birth_dates, error_generator=invalid_birth_date)

    if birth_of_date:
        age = datetime.now().year - birth_of_date.year
    else:
        age = None

    user_info_data = {
        "id": user_id,
        "username": username,
        "real_name": real_name,
        "phone_number": phone_number,
        "sex": sex,
        "job": job,
        "company": company,
        "email": email,
        "password": password,
        "birth_of_date": birth_of_date,
        "age": age,
        "create_time": create_time,
        "delete_time": delete_time
    }
    return user_info_data