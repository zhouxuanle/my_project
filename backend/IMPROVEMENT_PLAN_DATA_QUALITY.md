# Data Quality Improvement Plan for generate_event_tracking_data.py

## Overview
This plan outlines the improvements to enhance data quality in the data generation methods. Each table method will be updated to generate up to 100,000 records with a mix of realistic and erroneous data (20-40% erroneous). The goal is to simulate real-world data scenarios for testing and validation.

Key requirements:
- Data volume: Up to 100,000 records per table
- Error injection: 20-40% of data should contain intentional errors or invalid values
- Uniqueness: Fields capable of having 100,000 unique values will have dedicated data files
- Code structure: Each method remains under 20 lines, importing data from organized folders
- Folder structure: Create dedicated folders for each table containing code and data files

## General Approach
1. Analyze each field in every table to determine uniqueness potential
2. For fields with high uniqueness potential (>100k possible unique values), create text files with 100k unique entries
3. For fields with limited uniqueness, handle in code with controlled repetition or limited sets
4. Implement error injection logic to introduce 20-40% invalid data
5. Restructure code to import from table-specific modules
6. Maintain method simplicity (<20 lines each)

## Progress Tracking
- [x] User Table: Analysis complete, implementation complete
- [x] Address Table: Analysis complete, implementation complete
- [x] Categories Table: Analysis complete, implementation complete
- [x] Subcategories Table: Analysis complete, implementation complete
- [x] Products Table: Analysis complete, implementation complete
- [x] Product SKU Table: Analysis complete, implementation complete
- [x] Wishlist Table: Analysis complete, implementation complete
- [x] Order Details Table: Analysis complete, implementation complete
- [x] Order Item Table: Analysis complete, implementation complete
- [x] Payment Details Table: Analysis complete, implementation complete

## Folder Structure
```
backend/data_generators/
├── user_table/
│   ├── user_data.py
│   ├── data/
│   │   ├── usernames.txt (100k unique)
│   │   ├── real_names.txt (100k unique)
│   │   ├── phone_numbers.txt (100k unique)
│   │   ├── emails.txt (100k unique)
│   │   ├── passwords.txt (100k unique)
│   │   ├── jobs.txt (100k unique)
│   │   ├── companies.txt (100k unique)
│   │   └── birth_dates.txt (46k unique, max possible)
├── address_table/
│   ├── address_data.py
│   ├── data/
│   │   ├── address_lines.txt (100k unique)
│   │   ├── postal_codes.txt (100k unique)
│   │   ├── cities.txt (100k unique)
│   │   └── countries.txt (139 unique, max possible)
├── categories_table/
│   ├── categories_data.py
│   ├── data/
│   │   └── category_names.txt (210 unique, max possible with variations)
│   └── ...
├── subcategories_table/
│   ├── subcategories_data.py
│   └── ...
├── products_table/
│   ├── products_data.py
│   └── ...
├── product_sku_table/
│   ├── sku_data.py
│   └── ...
├── wishlist_table/
│   ├── wishlist_data.py
│   └── ...
├── order_details_table/
│   ├── order_details_data.py
│   └── ...
├── order_item_table/
│   ├── order_item_data.py
│   └── ...
├── payment_details_table/
│   ├── payment_details_data.py
│   └── ...
└── ...
```

## User Table Analysis
Fields in user_info table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| username | 100k+ unique | Faker + custom file | Create usernames.txt |
| real_name | 100k+ unique | Faker + custom file | Create real_names.txt |
| phone_number | 100k+ unique | Faker + custom file | Create phone_numbers.txt |
| sex | 3 unique | Code enum | male, female, other |
| job | ~100 unique | Faker + custom file | Limited, create jobs.txt with ~100 |
| company | ~100 unique | Faker + custom file | Limited, create companies.txt with ~100 |
| email | 100k+ unique | Faker + custom file | Create emails.txt |
| password | 100k+ unique | Faker + custom file | Create passwords.txt |
| birth_of_date | 100k+ unique | Faker + custom file | Create birth_dates.txt |
| age | Calculated | Code | Derived from birth date |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for user table:
- username: 20-40% invalid (numbers, special chars, empty)
- real_name: 20-40% invalid (non-name strings, numbers)
- phone_number: 20-40% invalid formats
- sex: 20-40% invalid values (numbers, random strings)
- job: 20-40% invalid (non-job strings)
- company: 20-40% invalid (non-company strings)
- email: 20-40% invalid formats
- password: 20-40% invalid (too short, no complexity)
- birth_of_date: 20-40% future dates or invalid
- age: Handled via birth date errors

## Implementation Steps for User Table
1. Create backend/data_generators/user_table/ folder
2. Create data/ subfolder
3. Generate data files with 100k unique values where applicable
4. Create user_data.py module with data loading and generation logic
5. Update generate_user_data() method to import and use the new module
6. Test for 100k records with proper error distribution

## Next Steps
After user table completion and user approval, proceed to address table following similar pattern.

## Address Table Analysis
Fields in address table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| user_id | From user | Parameter | Links to user |
| title | 5 unique | Code list | Home, Work, etc. |
| address_line | 100k+ unique | Faker + custom file | Create address_lines.txt |
| country | ~200 unique | Faker + custom file | Limited, create countries.txt with ~200 |
| city | 100k+ unique | Faker + custom file | Create cities.txt with 100k unique |
| postal_code | 100k+ unique | Faker + custom file | Create postal_codes.txt |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for address table:
- address_line: 20-40% invalid (non-address strings, numbers)
- country: 20-40% invalid (non-country strings)
- city: 20-40% invalid (non-city strings, numbers)
- postal_code: 20-40% invalid formats
- title: 20-40% invalid (non-title strings)

## Categories Table Analysis
Fields in categories table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| name | ~210 unique | Faker + custom file | Limited, create category_names.txt with ~210 |
| description | Generated | Code | Related to category name |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for categories table:
- name: 20-40% invalid (non-category strings, numbers)
- description: 20-40% invalid (non-description strings); valid descriptions are contextually related to the category name

## Subcategories Table Analysis
Fields in subcategories table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| parent_id | From category | Parameter | Links to category |
| name | 100k+ unique | Generated | Related to parent category |
| description | Generated | Code | Related to subcategory name |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for subcategories table:
- name: 20-40% invalid (non-subcategory strings)
- description: 20-40% invalid (non-description strings); valid entries are contextually related to the parent category

## Products Table Analysis
Fields in products table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| name | 100k+ unique | Generated | Related to subcategory |
| description | Generated | Code | Related to product name and subcategory |
| category_id | From subcategory | Parameter | Links to subcategory (note: field name might be subcategory_id) |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for products table:
- name: 20-40% invalid (non-product strings)
- description: 20-40% invalid (non-description strings); valid entries are contextually related to the subcategory

## Product SKU Table Analysis
Fields in product_sku table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | Generated | Composite from category/subcategory/product IDs + sku_number |
| product_id | From product | Parameter | Links to product |
| price | Variable | Random | 5.0-500.0 range |
| quantity | Variable | Random | 0-9,999,999 range |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for product SKU table:
- price: 20-40% invalid (negative, non-numeric)
- quantity: 20-40% invalid (negative, non-integer)

## Wishlist Table Analysis
Fields in wishlist table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| user_id | From user | Parameter | Links to user |
| products_sku_id | From SKU | Parameter | Links to product SKU |
| create_time | N/A | Code | Current timestamp |
| delete_time | N/A | Code | Random future date |

Error injection for wishlist table:
- user_id: 20-40% invalid (non-UUID strings)
- products_sku_id: 20-40% invalid (non-SKU strings)

## Order Details Table Analysis
Fields in order_details table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| user_id | From user | Parameter | Links to user |
| payment_id | From payment | Parameter | Links to payment |
| create_time | N/A | Code | Current timestamp |
| updated_at | N/A | Code | Random future date |

Error injection for order details table:
- user_id: 20-40% invalid (non-UUID strings)
- payment_id: 20-40% invalid (non-UUID strings)

## Order Item Table Analysis
Fields in order_item table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| order_id | From order | Parameter | Links to order |
| products_sku_id | From SKU | Parameter | Links to product SKU |
| quantity | Variable | Random | 1-99,999,999 range |
| create_time | N/A | Code | Current timestamp |
| updated_at | N/A | Code | Random future date |

Error injection for order item table:
- order_id: 20-40% invalid (non-UUID strings)
- products_sku_id: 20-40% invalid (non-SKU strings)
- quantity: 20-40% invalid (negative, non-integer)

## Payment Details Table Analysis
Fields in payment_details table:

| Field | Uniqueness Potential | Data Source | Notes |
|-------|---------------------|-------------|-------|
| id | 100k+ unique | UUID generation | Always unique |
| amount | Fixed | Code | Set to 0 (calculated later by Spark) |
| provider | Variable | Faker | Credit card provider names |
| status | Limited | Code list | Success, Pending, Failed, Refunded |
| create_time | N/A | Code | Current timestamp |
| updated_at | N/A | Code | Random future date |

Error injection for payment details table:
- amount: 20-40% invalid (negative, non-numeric)
- provider: 20-40% invalid (non-provider strings)
- status: 20-40% invalid (non-status strings)</content>
<parameter name="filePath">d:\study\my_project\backend\IMPROVEMENT_PLAN_DATA_QUALITY.md