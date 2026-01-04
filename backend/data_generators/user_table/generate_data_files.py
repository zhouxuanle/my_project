import random
from faker import Faker
from datetime import datetime, date
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

# Generate usernames
print("Generating usernames...")
usernames = generate_unique_list(lambda: fake.user_name(), 100000)
with open('data/usernames.txt', 'w') as f:
    for name in usernames:
        f.write(name + '\n')

# Generate real names
print("Generating real names...")
real_names = generate_unique_list(lambda: fake.name(), 100000)
with open('data/real_names.txt', 'w') as f:
    for name in real_names:
        f.write(name + '\n')

# Generate phone numbers
print("Generating phone numbers...")
phone_numbers = generate_unique_list(lambda: fake.phone_number(), 100000)
with open('data/phone_numbers.txt', 'w') as f:
    for num in phone_numbers:
        f.write(num + '\n')

# Generate emails
print("Generating emails...")
emails = generate_unique_list(lambda: fake.email(), 100000)
with open('data/emails.txt', 'w') as f:
    for email in emails:
        f.write(email + '\n')

# Generate passwords
print("Generating passwords...")
passwords = generate_unique_list(lambda: fake.password(), 100000)
with open('data/passwords.txt', 'w') as f:
    for pwd in passwords:
        f.write(pwd + '\n')

# Generate jobs (aim for 100k unique realistic variations)
print("Generating jobs...")
base_jobs = set()
while len(base_jobs) < 100:
    base_jobs.add(fake.job())
base_jobs = list(base_jobs)

prefixes = ["Senior", "Junior", "Lead", "Principal", "Associate", "Chief", "Vice President", "Manager", "Director", "Analyst", "Engineer", "Developer", "Consultant", "Specialist", "Coordinator", "Assistant", "Supervisor", "Officer", "Administrator", "Technician", "Executive", "Intern", "Trainee", "Head", "Deputy"]

jobs = []
for prefix in prefixes:
    for base in base_jobs:
        jobs.append(f"{prefix} {base}")
        if len(jobs) >= 100000:
            break
    if len(jobs) >= 100000:
        break

while len(jobs) < 100000:
    jobs.append(f"Professional {len(jobs) - len(prefixes)*len(base_jobs) + 1}")

random.shuffle(jobs)
with open('data/jobs.txt', 'w') as f:
    for job in jobs:
        f.write(job + '\n')

# Generate companies (aim for 100k unique realistic variations)
print("Generating companies...")
base_companies = set()
while len(base_companies) < 100:
    base_companies.add(fake.company())
base_companies = list(base_companies)

suffixes = ["Inc", "LLC", "Corp", "Ltd", "Group", "Enterprises", "Solutions", "Technologies", "Systems", "Services", "Consulting", "Partners", "Associates", "Holdings", "Ventures", "Industries", "Corporation", "Company", "Agency", "Studio"]

companies = []
for suffix in suffixes:
    for base in base_companies:
        companies.append(f"{base} {suffix}")
        if len(companies) >= 100000:
            break
    if len(companies) >= 100000:
        break

while len(companies) < 100000:
    companies.append(f"Business Entity {len(companies) - len(suffixes)*len(base_companies) + 1}")

random.shuffle(companies)
with open('data/companies.txt', 'w') as f:
    for comp in companies:
        f.write(comp + '\n')

# Generate birth dates (maximize unique by expanding range)
print("Generating birth dates...")
birth_dates = []
for _ in range(100000):
    birth_dates.append(fake.date_of_birth(minimum_age=0, maximum_age=150))
# To maximize unique, but still limited, we'll have duplicates
with open('data/birth_dates.txt', 'w') as f:
    for bd in birth_dates:
        f.write(bd.isoformat() + '\n')

print("All data files generated successfully!")