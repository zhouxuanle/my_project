# Data Quality Error Summary - Data Generators

## Overview
This document catalogs all potential error data values and types detected across the data generation pipeline. This information is essential for improving the data cleaning pipeline. Each table's error patterns are documented with specific error values and types that may appear in the generated datasets.

---

## 1. Address Table (`address_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `address_id-{uuid}` | Valid (UUID format enforced) |
| `user_id` | String | Valid user IDs from user table | Valid (references valid user) |
| `title` | String | Home Address, Work Address, Billing Address, Shipping Address, Vacation Home | `Invalid Title {1-10}` |
| `address_line` | String | Real address lines from data file | `Invalid Address {1-1000}` |
| `country` | String | Valid countries from data file | Valid (reference enforced) |
| `city` | String | Valid cities from data file (matched to country) | Valid (reference enforced) |
| `postal_code` | String | Valid postal codes from data file | `INVALID{100-999}` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `title`: Malformed string pattern (Invalid Title + random number)
  - `address_line`: Malformed string pattern (Invalid Address + random number)
  - `postal_code`: Invalid format with prefix "INVALID" + numbers

### Common Error Scenarios
1. Invalid titles not in predefined list
2. Address lines that don't match expected format
3. Mismatched postal codes

---

## 2. Categories Table (`categories_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `category_id-{uuid}` | Valid (UUID format enforced) |
| `name` | String | Category names from data file | `Invalid Category {1-1000}` |
| `description` | String | Related description to category | `Invalid description {1-1000}` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `name`: Malformed string pattern (Invalid Category + random number)
  - `description`: Malformed string pattern (Invalid description + random number)

### Common Error Scenarios
1. Category names not in predefined list
2. Descriptions that don't relate to valid category
3. Invalid category-description pairs

---

## 3. Order Details Table (`order_details_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `order_details_id-{uuid}` | Valid (UUID format enforced) |
| `user_id` | String | Valid user IDs | `invalid-user-{1-1000}` |
| `payment_id` | String | Valid payment IDs | `invalid-payment-{1-1000}` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `updated_at` | DateTime | Current + 0-30 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `user_id`: Orphaned reference - invalid-user pattern (does not exist in user table)
  - `payment_id`: Orphaned reference - invalid-payment pattern (does not exist in payment table)

### Common Error Scenarios
1. Referential integrity violations - user_id doesn't exist
2. Referential integrity violations - payment_id doesn't exist
3. Foreign key constraint failures

---

## 4. Order Item Table (`order_item_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `order_item_id-{uuid}` | Valid (UUID format enforced) |
| `order_id` | String | Valid order IDs | `invalid-order-{1-1000}` |
| `products_sku_id` | String | Valid SKU IDs | `invalid-sku-{1-1000}` |
| `quantity` | Integer | 1-99999999 | `-50`, `"invalid"` (string), `None`, `999999999` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `updated_at` | DateTime | Current + 0-30 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `order_id`: Orphaned reference (invalid-order pattern)
  - `products_sku_id`: Orphaned reference (invalid-sku pattern)
  - `quantity`: **Multiple error types**
    - Negative values: `-50`
    - Wrong type: String `"invalid"` instead of integer
    - Null/None values
    - Excessive values: `999999999` (unrealistic quantity)

### Common Error Scenarios
1. Foreign key violations (order, SKU references)
2. Type mismatch in quantity field
3. Invalid business logic (negative quantities)
4. Out-of-range values (extremely large quantities)
5. Missing values (None)

---

## 5. Payment Details Table (`payment_details_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `payment_details_id-{uuid}` | Valid (UUID format enforced) |
| `amount` | Float | 0.00 - 500.00 | `-100.0`, `"invalid"` (string), `None`, `9999999.99` |
| `provider` | String | Credit card provider names | `Invalid Provider {1-1000}` |
| `status` | String | Success, Pending, Failed, Refunded | `Invalid Status {1-1000}` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `updated_at` | DateTime | Current + 0-30 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `amount`: **Multiple error types**
    - Negative values: `-100.0` (invalid for payment)
    - Wrong type: String `"invalid"` instead of float
    - Null/None values
    - Excessive values: `9999999.99` (unrealistic amount)
  - `provider`: Malformed string pattern (Invalid Provider + random number)
  - `status`: Invalid enumeration values (Invalid Status + random number)

### Common Error Scenarios
1. Type mismatch in amount field
2. Invalid business logic (negative amounts)
3. Out-of-range values (extremely large amounts)
4. Invalid payment provider names
5. Invalid payment status values (not in enum)
6. Missing values (None)

---

## 6. Products Table (`products_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `product_id-{uuid}` | Valid (UUID format enforced) |
| `name` | String | Generated product names related to subcategory | `Invalid Product {1-1000}` |
| `description` | String | Related description to product | `Invalid description {1-1000}` |
| `category_id` | String | Valid subcategory IDs | Valid (references subcategory) |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `name`: Malformed string pattern (Invalid Product + random number)
  - `description`: Malformed string pattern (Invalid description + random number)

### Common Error Scenarios
1. Product names not matching subcategory
2. Descriptions not related to product
3. Generic or invalid product names
4. Inconsistent product-description pairs

---

## 7. Product SKU Table (`product_sku_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `{category-3digits}-{subcategory-3digits}-{product-3digits}-{random-5digits}` | Valid (composite key format enforced) |
| `product_id` | String | Valid product IDs | Valid (references product) |
| `price` | Float | 5.00 - 500.00 | `-50.0`, `"invalid"` (string), `None`, `999999.99` |
| `quantity` | Integer | 0 - 9999999 | `-100`, `"invalid"` (string), `None`, `99999999` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `price`: **Multiple error types**
    - Negative values: `-50.0` (invalid for pricing)
    - Wrong type: String `"invalid"` instead of float
    - Null/None values
    - Excessive values: `999999.99` (unrealistic price)
  - `quantity`: **Multiple error types**
    - Negative values: `-100`
    - Wrong type: String `"invalid"` instead of integer
    - Null/None values
    - Excessive values: `99999999` (unrealistic inventory)

### Common Error Scenarios
1. Type mismatch in price and quantity fields
2. Invalid business logic (negative price/quantity)
3. Out-of-range values (extremely large values)
4. Missing values (None)
5. Inconsistent pricing across duplicate products

---

## 8. Subcategories Table (`subcategories_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `subcategory_id-{uuid}` | Valid (UUID format enforced) |
| `parent_id` | String | Valid category IDs | Valid (references category) |
| `name` | String | Generated subcategory names related to category | `Invalid Subcategory {1-1000}` |
| `description` | String | Related description to subcategory | `Invalid description {1-1000}` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `name`: Malformed string pattern (Invalid Subcategory + random number)
  - `description`: Malformed string pattern (Invalid description + random number)

### Common Error Scenarios
1. Subcategory names not matching parent category
2. Descriptions not related to subcategory
3. Invalid subcategory-description pairs
4. Missing parent category relationships

---

## 9. User Table (`user_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `user_id-{uuid}` | Valid (UUID format enforced) |
| `username` | String | Valid usernames from data file | `{1000-9999}@invalid` |
| `real_name` | String | Valid names from data file | `InvalidName{1-1000}` |
| `phone_number` | String | Valid phone numbers from data file | `invalid-phone-{1-1000}` |
| `sex` | String | male, female, other | `unknown`, `123` (wrong type), empty string `""` |
| `job` | String | Valid jobs from data file | `Invalid Job {1-100}` |
| `company` | String | Valid companies from data file | `Invalid Company {1-100}` |
| `email` | String | Valid emails from data file | `invalid.email{1-1000}@bad` |
| `password` | String | Valid passwords from data file | `123` (too simple/weak) |
| `birth_of_date` | Date | Historical dates from data file | Future date (date.today() + 1-3650 days) |
| `age` | Integer | Calculated from birth_of_date | `None` (if birth_of_date is None) |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `username`: Malformed format with invalid pattern
  - `real_name`: Malformed string pattern
  - `phone_number`: Malformed string pattern (invalid-phone)
  - `sex`: **Multiple error types**
    - Invalid enumeration: `unknown`
    - Type mismatch: `123` (numeric instead of string)
    - Empty string: `""`
  - `job`: Malformed string pattern
  - `company`: Malformed string pattern
  - `email`: Invalid email format (missing proper domain)
  - `password`: Security concern (too simple - only 3 characters)
  - `birth_of_date`: **Critical error** - Future dates (violates business logic)
  - `age`: Null when birth date is invalid

### Common Error Scenarios
1. Invalid email format/domain
2. Weak password values
3. Invalid sex/gender values
4. Invalid phone number format
5. Invalid username format
6. Future birth dates (data validation error)
7. Age calculation errors due to invalid birth date
8. Personally identifiable information (PII) data quality issues

---

## 10. Wishlist Table (`wishlist_table/`)

### Schema Fields & Error Patterns

| Field | Data Type | Expected Values | Error Values/Types |
|-------|-----------|-----------------|-------------------|
| `id` | String | `wishlist_id-{uuid}` | Valid (UUID format enforced) |
| `user_id` | String | Valid user IDs | `invalid-user-{1-1000}` |
| `products_sku_id` | String | Valid SKU IDs | `invalid-sku-{1-1000}` |
| `create_time` | DateTime | Current timestamp | Valid (system generated) |
| `delete_time` | DateTime | Random date within 1-365 days | Valid (system generated) |

### Error Summary
- **Error Rate**: ~30% per field
- **Critical Fields with Errors**:
  - `user_id`: Orphaned reference (invalid-user pattern)
  - `products_sku_id`: Orphaned reference (invalid-sku pattern)

### Common Error Scenarios
1. Foreign key violations (user reference)
2. Foreign key violations (SKU reference)
3. Orphaned wishlist items without valid user
4. Orphaned wishlist items without valid SKU

---

## Error Classification Summary

### By Severity Level

#### 🔴 **CRITICAL** (Data Integrity & Logic)
1. **Foreign Key Violations**: order_details, order_item, wishlist tables
   - Invalid user_id, payment_id, order_id, sku_id references
2. **Future Dates**: User birth_of_date field
3. **Negative Values**: price, quantity, amount fields
4. **Invalid Enumerations**: status, sex fields with non-enum values

#### 🟠 **HIGH** (Type Mismatch & Business Logic)
1. **Type Mismatches**: quantity, price, amount fields containing strings or None
2. **Out-of-Range Values**: Extremely large quantity/price/amount values
3. **Invalid Format**: email addresses, phone numbers, usernames
4. **Security Issues**: Weak password values

#### 🟡 **MEDIUM** (Data Consistency & Validation)
1. **Invalid Text Patterns**: Names, titles, descriptions starting with "Invalid..."
2. **Missing Relationships**: Subcategories without valid category references
3. **Inconsistent Pairs**: Product-description, category-description mismatches

#### 🟢 **LOW** (Data Quality)
1. **Generic Values**: Placeholder error strings
2. **Timestamp Issues**: delete_time before create_time (potential)
3. **Empty Strings**: Empty sex field values

### By Error Type

| Error Type | Fields Affected | Count | Examples |
|-----------|-----------------|-------|----------|
| Orphaned Foreign Key | user_id, payment_id, order_id, sku_id | 8+ | `invalid-user-123`, `invalid-sku-456` |
| Type Mismatch | price, quantity, amount | 3 | `"invalid"`, `None` |
| Invalid Enumeration | status, sex | 2 | `"Invalid Status"`, `"123"` |
| Malformed String | name, title, description | 6+ | `Invalid Category 123`, `Invalid Address` |
| Negative Value | price, quantity, amount | 3 | `-50.0`, `-100` |
| Out-of-Range | price, quantity, amount | 3 | `999999.99`, `99999999` |
| Invalid Format | email, phone, username | 3 | `invalid.email@bad`, `invalid-phone-1` |
| Future Date | birth_of_date | 1 | Future dates |
| Security Issue | password | 1 | `"123"` (too weak) |
| Empty/Null | sex, password, all text fields | 10+ | `""`, `None` |

---

## Data Cleaning Pipeline Recommendations

### Priority Actions

1. **Referential Integrity Checks** (CRITICAL)
   - Validate all foreign key references before insert/update
   - Remove orphaned records or cascade delete appropriately

2. **Type Validation** (HIGH)
   - Enforce strict type checking for numeric fields
   - Convert string representations to proper types or flag as errors

3. **Range Validation** (HIGH)
   - Implement min/max bounds for price, quantity, amount
   - Reject negative values in financial/inventory fields

4. **Format Validation** (HIGH)
   - Email format validation (RFC 5322)
   - Phone number format validation (E.164)
   - UUID format validation
   - Date format validation

5. **Enumeration Validation** (MEDIUM)
   - Create validation lists for fixed-value fields (status, sex)
   - Reject values outside valid sets

6. **Business Logic Validation** (MEDIUM)
   - Ensure birth_of_date is in the past
   - Verify product-subcategory relationships
   - Validate delete_time > create_time

7. **String Pattern Validation** (MEDIUM)
   - Reject strings containing "Invalid" patterns
   - Implement whitelist validation for categories/descriptions

8. **Data Relationship Validation** (LOW)
   - Verify category-subcategory-product hierarchy
   - Validate payment-order relationships

---

## Implementation Checklist

- [ ] Add foreign key constraint checks
- [ ] Implement numeric field type validation
- [ ] Add min/max validation for prices, quantities
- [ ] Implement email/phone format validation
- [ ] Create enum validation for fixed fields
- [ ] Add date logic validation (past dates)
- [ ] Implement string pattern filters
- [ ] Add null/empty field handling
- [ ] Create audit logging for rejected records
- [ ] Build data quality metrics dashboard
- [ ] Document exception handling procedures

