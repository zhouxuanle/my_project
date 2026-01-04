# My Project - E-commerce Data Generation Platform

A full-stack web application for generating and managing e-commerce data with real-time processing capabilities. Built with Flask backend, React frontend, and Azure cloud services.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [License](#license)

## Overview

This platform enables users to generate realistic e-commerce data including users, products, orders, payments, and related entities. It supports both synchronous and asynchronous data generation workflows, with real-time progress notifications via SignalR.

### Key Capabilities

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Data Generation**: Generate realistic e-commerce data using Faker library
- **Synchronous Processing**: Direct database writes for small datasets
- **Asynchronous Processing**: Queue-based batch processing for large datasets via Azure Functions
- **Real-time Updates**: SignalR integration for job status notifications
- **Data Storage**: MySQL database for structured data, Azure Blob Storage for raw data
- **RESTful API**: Comprehensive API endpoints for all operations

## Features

### Backend Features

- User registration and authentication with JWT tokens
- Token refresh mechanism for seamless user experience
- Fake data generation for 11+ e-commerce entities (users, products, orders, etc.)
- Database connection pooling for efficient resource management
- Azure Queue Storage integration for async job processing
- Azure Blob Storage for raw data persistence
- SOCKS5 proxy support with selective bypass for Azure services
- Comprehensive error handling and logging

### Frontend Features

- React-based single-page application
- User authentication flow (login/register)
- Protected routes with JWT authentication
- Data generation interface with progress tracking
- Real-time job status updates via SignalR
- Multiple data table views (users, products, orders, etc.)
- Responsive UI built with Tailwind CSS
- State management with Zustand

## Architecture

The application follows a three-tier architecture:

```
┌─────────────────┐
│   React Frontend │
│   (Vite + React) │
└────────┬────────┘
         │ HTTP/SignalR
┌────────▼────────┐
│  Flask Backend   │
│  (RESTful API)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼──────────┐
│ MySQL│  │ Azure Services│
│  DB  │  │ - Queue       │
└──────┘  │ - Blob        │
          │ - Functions   │
          │ - SignalR     │
          └───────────────┘
```

### Data Flow

1. **Synchronous Mode**: User → Frontend → Backend API → MySQL Database → Response
2. **Asynchronous Mode**: User → Frontend → Backend API → Azure Queue → Azure Function → Blob Storage + SignalR Notification → User

## Tech Stack

### Backend

- **Framework**: Flask 2.3.0+
- **Database**: MySQL with PyMySQL
- **Authentication**: Flask-JWT-Extended
- **Data Generation**: Faker, faker-commerce
- **Cloud Services**: Azure Storage (Queue, Blob), Azure Functions, Azure SignalR
- **Connection Pooling**: DBUtils
- **Proxy Support**: PySocks

### Frontend

- **Framework**: React 19.2.0
- **Build Tool**: Vite 4.5.0
- **Routing**: React Router DOM 6.8.0
- **Styling**: Tailwind CSS 3.3.5
- **State Management**: Zustand 5.0.9
- **Real-time**: @microsoft/signalr 8.0.0
- **Authentication**: jwt-decode 4.0.0

### Infrastructure

- **Database**: Azure Database for MySQL
- **Storage**: Azure Blob Storage, Azure Queue Storage
- **Serverless**: Azure Functions (Python)
- **Real-time Communication**: Azure SignalR Service
- **Development**: Python virtual environments, npm

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- MySQL database (Azure Database for MySQL recommended)
- Azure account (for cloud features)
- Git

## Installation

### Clone the Repository

```bash
git clone https://github.com/zhouxuanle/my_project.git
cd my_project
```

### Backend Setup

1. Create and activate a virtual environment:

```bash
# Windows
python -m venv my_env
my_env\Scripts\activate

# macOS/Linux
python3 -m venv my_env
source my_env/bin/activate
```

2. Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Configure environment variables (see [Configuration](#configuration))

### Frontend Setup

1. Install Node.js dependencies:

```bash
cd frontend
npm install
```

### Azure Functions Setup (Optional, for async processing)

1. Install Azure Functions dependencies:

```bash
cd backend/myfunc
pip install -r requirements.txt
```

2. Install Azure Functions Core Tools (if not already installed)

## Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DB_HOST=your-mysql-host.mysql.database.azure.com
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes in seconds
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7  # 7 days

# Azure Configuration (for async processing)
AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string
AZURE_SIGNALR_CONNECTION_STRING=your-azure-signalr-connection-string

# Proxy Configuration (optional)
PROXY_HOST=127.0.0.1
PROXY_PORT=7890
```

### Frontend Configuration

The frontend connects to the backend API. Update the API base URL in `/frontend/src/config` if needed.

### Azure Functions Configuration

Create a `local.settings.json` file in the `backend/myfunc` directory:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "your-azure-storage-connection-string",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_SIGNALR_CONNECTION_STRING": "your-azure-signalr-connection-string"
  }
}
```

### Database Schema

The application requires the following MySQL tables:

- `app_users` - Application user accounts
- `users` - Generated user data
- `addresses` - User addresses
- `categories` - Product categories
- `sub_categories` - Product subcategories
- `products` - Product information
- `products_skus` - Product SKUs with pricing and stock
- `order_details` - Order information
- `order_item` - Order line items
- `payment_details` - Payment transactions
- `wishlist` - User wishlists

## Usage

### Starting the Application

#### Backend

```bash
cd backend
python app.py
```

The Flask server will start on `http://localhost:5000` (or the port specified in your configuration).

#### Frontend

```bash
cd frontend
npm run dev
```

The React development server will start on `http://localhost:3000`.

#### Azure Functions (for async processing)

```bash
cd backend/myfunc
func start
```

### Basic Workflow

1. **Register/Login**: Create an account or log in to the application
2. **Generate Data**: 
   - Choose synchronous mode for small datasets (< 1000 records)
   - Choose asynchronous mode for large datasets (1000+ records)
3. **View Data**: Browse generated data in various table views
4. **Monitor Jobs**: Track asynchronous job progress in real-time

## API Documentation

### Authentication Endpoints

#### POST `/register`
Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "msg": "User created successfully"
}
```

#### POST `/login`
Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "user_id": "string"
}
```

#### POST `/refresh`
Refresh access token using refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "access_token": "string"
}
```

### Data Generation Endpoints

#### POST `/write_to_db`
Synchronously generate and write data to the database.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "dataCount": 100
}
```

**Response:**
```json
{
  "success": true,
  "message": "your user name is : username",
  "user_id": "user_id-uuid",
  "all_messages": ["array of messages"],
  "all_user_ids": ["array of user IDs"],
  "generation_time": 0.1234,
  "commit_time": 0.5678
}
```

#### GET `/get_<table_name>`
Retrieve data from a specific table. Available tables: `user`, `address`, `category`, `subcategory`, `product`, `products_sku`, `wishlist`, `payment`, `order`, `order_item`.

**Example:**
```
GET /get_user
GET /get_product
```

**Response:**
```json
{
  "success": true,
  "user": [
    {
      "id": "user_id-uuid",
      "user_name": "username",
      ...
    }
  ]
}
```

### Async Job Endpoints

#### POST `/generate_raw`
Queue an asynchronous data generation job.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "dataCount": 10000
}
```

**Response:**
```json
{
  "parentJobId": "uuid",
  "jobIds": ["uuid1", "uuid2", ...],
  "status": "queued",
  "total_count": 10000,
  "batch_size": 1000,
  "total_chunks": 10
}
```

#### GET `/get_raw_data/<parent_job_id>/<table_name>`
Retrieve raw data from blob storage for a specific job.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "user": [
    {
      "id": "user_id-uuid",
      ...
    }
  ]
}
```

#### GET `/list_parent_jobs`
List all parent job IDs for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "parentJobIds": ["uuid1", "uuid2", ...]
}
```

## Project Structure

```
my_project/
├── backend/                    # Flask backend application
│   ├── routes/                 # API route blueprints
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── data.py            # Data generation endpoints
│   │   └── jobs.py            # Async job endpoints
│   ├── myfunc/                # Azure Functions
│   │   ├── function_app.py   # Function definitions
│   │   └── requirements.txt  # Function dependencies
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection pool
│   ├── utils.py               # Utility functions (proxy setup)
│   ├── generate_event_tracking_data.py  # Data generation logic
│   └── requirements.txt       # Backend dependencies
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── stores/            # Zustand state stores
│   │   ├── services/          # API service functions
│   │   ├── config/            # Frontend configuration
│   │   ├── hooks/             # Custom React hooks
│   │   ├── utils/             # Utility functions
│   │   ├── App.jsx            # Main application component
│   │   └── index.jsx          # Application entry point
│   ├── index.html             # HTML template
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── package.json           # Frontend dependencies
├── DB/                         # Database scripts (if any)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Development

### Backend Development

1. Activate the virtual environment
2. Make changes to Python files
3. Flask will auto-reload in debug mode
4. Test endpoints using tools like Postman or curl

### Frontend Development

1. The Vite dev server supports hot module replacement
2. Changes are reflected immediately in the browser
3. Check browser console for errors

### Adding New API Endpoints

1. Create or modify route files in `backend/routes/`
2. Register blueprints in `backend/app.py`
3. Add corresponding API calls in frontend services
4. Update state management in Zustand stores

### Database Migrations

When modifying the database schema:

1. Update table definitions in your MySQL database
2. Update corresponding code in `generate_event_tracking_data.py`
3. Test data generation with the new schema

## Deployment

### Backend Deployment

Deploy the Flask backend to:
- Azure App Service
- AWS Elastic Beanstalk
- Google Cloud Run
- Or any Python-supporting hosting platform

### Frontend Deployment

Build the production bundle:

```bash
cd frontend
npm run build
```

Deploy the `dist` folder to:
- Azure Static Web Apps
- Netlify
- Vercel
- AWS S3 + CloudFront
- Or any static hosting service

### Azure Functions Deployment

Deploy from Visual Studio Code with Azure Functions extension, or use Azure CLI:

```bash
cd backend/myfunc
func azure functionapp publish <function-app-name>
```

### Environment Variables

Ensure all production environment variables are configured in your hosting platform's settings.

## Security Considerations

- JWT tokens expire after 15 minutes (configurable)
- Refresh tokens expire after 7 days (configurable)
- Passwords are hashed using Werkzeug's security functions
- Database connection pooling prevents resource exhaustion
- Input validation on all API endpoints
- CORS configured for frontend access
- SQL injection prevention through parameterized queries

## Troubleshooting

### Backend Issues

- **Database connection errors**: Verify database credentials and network access
- **Azure connection errors**: Check proxy configuration and Azure service credentials
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Frontend Issues

- **API connection errors**: Verify backend URL configuration
- **SignalR connection errors**: Check Azure SignalR configuration
- **Build errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### Azure Functions Issues

- **Function not triggering**: Verify queue message format and connection strings
- **Missing dependencies**: Ensure requirements.txt includes all necessary packages
- **Path errors**: Check sys.path modifications for imports

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is private and proprietary. All rights reserved.

## Contact

For questions or support, please contact the project maintainer.

---

**Note**: This is an active development project. Features and documentation may change frequently.
