import random
from faker import Faker
import uuid

fake = Faker('en_US')

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

# Generate address lines
print("Generating address lines...")
address_lines = generate_unique_list(lambda: f"{fake.street_address()} {fake.secondary_address()}", 100000)
with open('data/address_lines.txt', 'w') as f:
    for addr in address_lines:
        f.write(addr + '\n')

# Generate postal codes (custom to ensure 100k unique)
print("Generating postal codes...")
postal_codes = []
seen = set()
while len(postal_codes) < 100000:
    # Generate realistic postal codes: 5 digits or 5-4 format
    if random.random() < 0.5:
        pc = f"{random.randint(10000, 99999)}"
    else:
        pc = f"{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"
    if pc not in seen:
        seen.add(pc)
        postal_codes.append(pc)
with open('data/postal_codes.txt', 'w') as f:
    for pc in postal_codes:
        f.write(pc + '\n')

# Generate cities (aim for 100k unique realistic, tied to countries)
print("Generating cities...")
countries_and_locales = [
    ('United States', 'en_US'),
    ('United Kingdom', 'en_GB'),
    ('Canada', 'en_CA'),
    ('Germany', 'de_DE'),
    ('France', 'fr_FR'),
    ('Japan', 'ja_JP'),
    ('Australia', 'en_AU'),
    ('Brazil', 'pt_BR'),
    ('India', 'en_IN'),
    ('South Korea', 'ko_KR')
]

cities_100k = []
for country, locale in countries_and_locales:
    fake_loc = Faker(locale)
    country_cities = [fake_loc.city() for _ in range(10000)]
    cities_100k.extend(country_cities)

# Generate countries (10 selected countries, repeated to 100k)
print("Generating countries...")
countries = [c[0] for c in countries_and_locales]
countries_100k = countries * 10000

# Shuffle pairs to ensure randomness while keeping matches
pairs = list(zip(countries_100k, cities_100k))
random.shuffle(pairs)
countries_100k, cities_100k = zip(*pairs)

with open('data/countries.txt', 'w', encoding='utf-8') as f:
    for country in countries_100k:
        f.write(country + '\n')

with open('data/cities.txt', 'w', encoding='utf-8') as f:
    for city in cities_100k:
        f.write(city + '\n')

print("All address data files generated successfully!")