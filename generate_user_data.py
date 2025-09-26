from faker import Faker
import random
import uuid

# Initialize Faker
fake = Faker()
Faker.seed(4321)

def generate_user_data():
    """Generates a single user profile with unique user data."""

    # Faker's built-in profile provider includes name, username, and sex
    profile = fake.profile()
    
    # Generate age by picking a random number within a reasonable range
    age = fake.random_int(min=18, max=90)
    
    # Generate a unique integer for a user ID
    user_id = str(uuid.uuid4())

    return {
        "user_id": user_id,
        "username": profile['username'],
        "name": profile['name'],
        "phone_number": fake.phone_number(),
        "sex": profile['sex'],
        "job": profile['job'],
        "company": profile['company'],
        "address": profile['address'],
        "mail": profile['mail'],
        "birthdate": profile['birthdate'],
        "age": age
    }

# Generate and print a single user
user = generate_user_data()
for key, value in user.items():
    print(f"{key}: {value}")

# --- Example of generating multiple users ---
print("\n--- Generating a list of 5 unique users ---")
unique_users = []
for _ in range(5):
    unique_users.append(generate_user_data())

for user in unique_users:
    print(user)
