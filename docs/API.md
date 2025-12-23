# API Documentation

Complete API reference for the E-commerce Data Generation Platform.

## Base URL

```
http://localhost:5000  # Development
https://your-domain.com  # Production
```

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. Most endpoints require an `Authorization` header:

```
Authorization: Bearer <access_token>
```

### Token Lifecycle

- **Access Token**: Expires after 15 minutes (configurable)
- **Refresh Token**: Expires after 7 days (configurable)

Use the `/refresh` endpoint to obtain a new access token using your refresh token.

---

## Endpoints

### Authentication

#### Register User

Create a new user account.

**Endpoint:** `POST /register`

**Authentication:** None required

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePassword123"
}
```

**Success Response (201 Created):**
```json
{
  "msg": "User created successfully"
}
```

**Error Responses:**

400 Bad Request - Missing credentials:
```json
{
  "msg": "Username and password required"
}
```

400 Bad Request - User already exists:
```json
{
  "msg": "Username already exists"
}
```

500 Internal Server Error:
```json
{
  "msg": "Error creating user"
}
```

---

#### Login

Authenticate and receive JWT tokens.

**Endpoint:** `POST /login`

**Authentication:** None required

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000_johndoe"
}
```

**Error Responses:**

401 Unauthorized - Invalid credentials:
```json
{
  "msg": "Invalid username or password"
}
```

500 Internal Server Error:
```json
{
  "msg": "Login error"
}
```

---

#### Refresh Token

Get a new access token using a refresh token.

**Endpoint:** `POST /refresh`

**Authentication:** Required (refresh token)

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**

401 Unauthorized - Invalid or expired refresh token:
```json
{
  "msg": "Token refresh failed"
}
```

---

### Data Generation (Synchronous)

#### Write to Database

Generate and directly insert data into the MySQL database. Suitable for small to medium datasets (< 1000 records).

**Endpoint:** `POST /write_to_db`

**Authentication:** Required (access token)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "dataCount": 100
}
```

**Parameters:**
- `dataCount` (integer, optional): Number of records to generate. Default: 1

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "your user name is : johndoe123",
  "user_id": "user_id-550e8400-e29b-41d4-a716-446655440000",
  "all_messages": [
    "your user name is : johndoe123",
    "your user name is : janedoe456",
    ...
  ],
  "all_user_ids": [
    "user_id-550e8400-e29b-41d4-a716-446655440000",
    "user_id-6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    ...
  ],
  "generation_time": 1.2345,
  "commit_time": 2.3456
}
```

**Response Fields:**
- `success` (boolean): Operation success status
- `message` (string): Last generated username
- `user_id` (string): Last generated user ID
- `all_messages` (array): All generated usernames
- `all_user_ids` (array): All generated user IDs
- `generation_time` (float): Time taken to generate data (seconds)
- `commit_time` (float): Time taken to commit to database (seconds)

**Error Responses:**

401 Unauthorized - Missing or invalid token:
```json
{
  "msg": "Missing Authorization Header"
}
```

500 Internal Server Error:
```json
{
  "success": false,
  "message": "数据库操作失败: <error details>"
}
```

---

### Data Retrieval

#### Get Table Data

Retrieve the most recent records from a specific table.

**Endpoint:** `GET /get_<table_name>`

**Authentication:** None required

**Available Table Names:**
- `user` - User data
- `address` - Address data
- `category` - Category data
- `subcategory` - Subcategory data
- `product` - Product data
- `products_sku` - Product SKU data
- `wishlist` - Wishlist data
- `payment` - Payment details
- `order` - Order details
- `order_item` - Order items
- `cart` - Shopping cart data

**Example Request:**
```
GET /get_user
GET /get_product
GET /get_order
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "user": [
    {
      "id": "user_id-550e8400-e29b-41d4-a716-446655440000",
      "user_name": "johndoe123",
      "real_name": "John Doe",
      "phone_number": "+1-555-123-4567",
      "sex": "M",
      "job": "Software Engineer",
      "company": "Tech Corp",
      "email": "john@example.com",
      "birth_of_date": "1990-01-15",
      "age": 34,
      "created_at": "2024-01-20T10:30:00",
      "deleted_at": "2024-01-20T11:00:00"
    },
    ...
  ]
}
```

**Note:** Returns up to 20 most recent records ordered by `created_at` descending.

**Error Responses:**

400 Bad Request - Invalid table name:
```json
{
  "success": false,
  "message": "Invalid table name: invalid_table"
}
```

500 Internal Server Error:
```json
{
  "success": false,
  "message": "数据库操作失败: <error details>"
}
```

---

### Asynchronous Job Processing

#### Generate Raw Data

Queue an asynchronous data generation job. Suitable for large datasets (1000+ records). Data is generated by Azure Functions and stored in Azure Blob Storage.

**Endpoint:** `POST /generate_raw`

**Authentication:** Required (access token)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "dataCount": 10000
}
```

**Parameters:**
- `dataCount` (integer, optional): Number of records to generate. Default: 1

**Success Response (202 Accepted):**
```json
{
  "parentJobId": "550e8400-e29b-41d4-a716-446655440000",
  "jobIds": [
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    ...
  ],
  "status": "queued",
  "total_count": 10000,
  "batch_size": 1000,
  "total_chunks": 10
}
```

**Response Fields:**
- `parentJobId` (string): Parent job identifier for tracking
- `jobIds` (array): Individual chunk job identifiers
- `status` (string): Job status ("queued")
- `total_count` (integer): Total records to generate
- `batch_size` (integer): Records per chunk (1000)
- `total_chunks` (integer): Number of chunks

**Job Processing:**
1. Request creates multiple Azure Queue messages (chunks)
2. Azure Functions process each chunk independently
3. Generated data is stored in Azure Blob Storage
4. SignalR sends real-time notifications on completion
5. Data can be retrieved via `/get_raw_data` endpoint

**Error Responses:**

401 Unauthorized:
```json
{
  "msg": "Missing Authorization Header"
}
```

500 Internal Server Error - Azure service error (logged server-side)

---

#### Get Raw Data

Retrieve generated raw data from Azure Blob Storage for a specific job.

**Endpoint:** `GET /get_raw_data/<parent_job_id>/<table_name>`

**Authentication:** Required (access token)

**Headers:**
```
Authorization: Bearer <access_token>
```

**URL Parameters:**
- `parent_job_id` (string): Parent job ID from `/generate_raw` response
- `table_name` (string): Table name to retrieve (user, product, order, etc.)

**Example Request:**
```
GET /get_raw_data/550e8400-e29b-41d4-a716-446655440000/user
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "user": [
    {
      "id": "user_id-550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe123",
      "real_name": "John Doe",
      ...
    },
    ...
  ]
}
```

**Note:** Returns up to 100 records. Data is retrieved from multiple blob chunks if available.

**Error Responses:**

401 Unauthorized:
```json
{
  "msg": "Missing Authorization Header"
}
```

404 Not Found - Data not ready or not found:
```json
{
  "success": false,
  "message": "Data not found or not ready yet"
}
```

500 Internal Server Error:
```json
{
  "success": false,
  "message": "Error retrieving data: <error details>"
}
```

---

#### List Parent Jobs

List all parent job IDs for the authenticated user.

**Endpoint:** `GET /list_parent_jobs`

**Authentication:** Required (access token)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "parentJobIds": [
    "550e8400-e29b-41d4-a716-446655440000",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "7c9e6679-7425-40de-944b-e07fc1f90ae7"
  ]
}
```

**Response Fields:**
- `success` (boolean): Operation success status
- `parentJobIds` (array): Sorted list of parent job IDs

**Error Responses:**

401 Unauthorized:
```json
{
  "msg": "Missing Authorization Header"
}
```

500 Internal Server Error:
```json
{
  "success": false,
  "message": "Error listing parent jobs: <error details>"
}
```

---

## Data Models

### Generated Data Structure

Each data generation cycle creates the following related entities:

#### User
```json
{
  "id": "user_id-uuid",
  "username": "string",
  "real_name": "string",
  "phone_number": "string",
  "sex": "M/F",
  "job": "string",
  "company": "string",
  "email": "string",
  "password": "string",
  "birth_of_date": "date",
  "age": "integer",
  "create_time": "datetime",
  "delete_time": "datetime"
}
```

#### Address
```json
{
  "id": "address_id-uuid",
  "user_id": "user_id-uuid",
  "title": "string",
  "address_line": "string",
  "country": "string",
  "city": "string",
  "postal_code": "string",
  "create_time": "datetime",
  "delete_time": "datetime"
}
```

#### Category
```json
{
  "id": "category_id-uuid",
  "name": "string",
  "description": "string",
  "create_time": "datetime",
  "delete_time": "datetime"
}
```

#### Product
```json
{
  "id": "product_id-uuid",
  "name": "string",
  "description": "string",
  "category_id": "subcategory_id-uuid",
  "create_time": "datetime",
  "delete_time": "datetime"
}
```

#### Order
```json
{
  "id": "order_id-uuid",
  "user_id": "user_id-uuid",
  "payment_id": "payment_id-uuid",
  "create_time": "datetime",
  "updated_at": "datetime"
}
```

## Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted (async job queued) |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

## Rate Limiting

Currently, there are no rate limits enforced. However, consider the following best practices:

- Use asynchronous endpoints for large datasets (> 1000 records)
- Batch size is automatically set to 1000 records per chunk for async jobs
- Synchronous endpoints may timeout with very large datasets

## Real-time Notifications

The application uses Azure SignalR for real-time job status updates.

### SignalR Connection

Connect to: `/negotiate` endpoint (returns SignalR connection info)

### Events

**JobStatusUpdate**
```json
{
  "jobId": "parent_job_id",
  "status": "completed",
  "message": "All 10 chunks completed for parent job ..."
}
```

## Best Practices

1. **Token Management**: Store tokens securely, refresh before expiration
2. **Batch Size**: Use async endpoints for > 1000 records
3. **Error Handling**: Implement retry logic for network errors
4. **Data Retrieval**: Poll `/get_raw_data` after receiving SignalR completion notification
5. **Resource Cleanup**: Monitor blob storage usage, implement cleanup policies

## Examples

### Python Example

```python
import requests

BASE_URL = "http://localhost:5000"

# Register and login
def authenticate():
    # Register
    response = requests.post(f"{BASE_URL}/register", json={
        "username": "testuser",
        "password": "TestPass123"
    })
    
    # Login
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "testuser",
        "password": "TestPass123"
    })
    
    tokens = response.json()
    return tokens['access_token']

# Generate data
def generate_data(access_token, count=100):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(
        f"{BASE_URL}/write_to_db",
        json={"dataCount": count},
        headers=headers
    )
    return response.json()

# Usage
access_token = authenticate()
result = generate_data(access_token, 50)
print(f"Generated {len(result['all_user_ids'])} users")
```

### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:5000';

// Login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  return data.access_token;
}

// Generate data
async function generateData(accessToken, count = 100) {
  const response = await fetch(`${BASE_URL}/write_to_db`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ dataCount: count })
  });
  
  return await response.json();
}

// Usage
const accessToken = await login('testuser', 'TestPass123');
const result = await generateData(accessToken, 50);
console.log(`Generated ${result.all_user_ids.length} users`);
```

---

For more information, see the main [README.md](../README.md).
