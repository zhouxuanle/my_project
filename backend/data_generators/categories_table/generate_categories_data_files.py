import random
from faker import Faker
from faker_commerce import Provider as CommerceProvider
import uuid

fake = Faker('en_US')
fake.add_provider(CommerceProvider)

def generate_unique_list(generator_func, count, max_attempts=1000000):
    """Generate a list of unique values using a generator function."""
    seen = set()
    result = []
    attempts = 0
    while len(result) < count and attempts < max_attempts:
        value = generator_func()
        if value not in seen:
            seen.add(value)
            result.append(value)
        attempts += 1
    if len(result) < count:
        raise ValueError(f"Could not generate {count} unique values, only got {len(result)}")
    return result

# Generate category names (generate variations for more unique)
print("Generating category names...")
base_categories = []
for _ in range(50):
    base_categories.append(fake.ecommerce_category())
base_categories = list(set(base_categories))  # Unique base
print(f"Base categories: {len(base_categories)}")

# Generate variations
prefixes = ["", "Home & ", "Outdoor ", "Professional ", "Kids' ", "Luxury ", "Budget ", "Eco-Friendly ", "Smart ", "Vintage "]
category_names = []
for prefix in prefixes:
    for base in base_categories:
        category_names.append(f"{prefix}{base}")
category_names = list(set(category_names))  # Remove any duplicates
print(f"Total unique categories: {len(category_names)}")

# If still less than 100k possible, but for file, we'll have max unique
category_names_100k = category_names * (100000 // len(category_names)) + category_names[:100000 % len(category_names)]
random.shuffle(category_names_100k)
with open('data/category_names.txt', 'w') as f:
    for name in category_names_100k:
        f.write(name + '\n')

# Generate descriptions (100k unique)
print("Generating descriptions...")
descriptions = generate_unique_list(lambda: fake.text(max_nb_chars=50), 100000)
with open('data/descriptions.txt', 'w') as f:
    for desc in descriptions:
        f.write(desc + '\n')

print("All categories data files generated successfully!")