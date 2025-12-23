# Deployment Guide

Comprehensive guide for deploying the E-commerce Data Generation Platform to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Azure Setup](#azure-setup)
- [Database Setup](#database-setup)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [Azure Functions Deployment](#azure-functions-deployment)
- [Environment Configuration](#environment-configuration)
- [Post-Deployment](#post-deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:

- Azure subscription with sufficient credits
- Azure CLI installed (`az --version`)
- Git installed
- Node.js 14+ and npm
- Python 3.8+
- MySQL client (for database setup)

## Azure Setup

### 1. Create Resource Group

```bash
az login
az group create --name my-project-rg --location eastus
```

### 2. Create Azure Services

#### MySQL Database

```bash
az mysql flexible-server create \
  --resource-group my-project-rg \
  --name my-project-mysql \
  --location eastus \
  --admin-user adminuser \
  --admin-password <strong-password> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 20 \
  --version 8.0.21
```

Configure firewall:

```bash
# Allow Azure services
az mysql flexible-server firewall-rule create \
  --resource-group my-project-rg \
  --name my-project-mysql \
  --rule-name AllowAzure \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Allow your IP (for management)
az mysql flexible-server firewall-rule create \
  --resource-group my-project-rg \
  --name my-project-mysql \
  --rule-name AllowMyIP \
  --start-ip-address <your-ip> \
  --end-ip-address <your-ip>
```

#### Storage Account

```bash
az storage account create \
  --name myprojectstorage123 \
  --resource-group my-project-rg \
  --location eastus \
  --sku Standard_LRS
```

Get connection string:

```bash
az storage account show-connection-string \
  --name myprojectstorage123 \
  --resource-group my-project-rg \
  --output tsv
```

Create storage containers:

```bash
# Get storage key
STORAGE_KEY=$(az storage account keys list \
  --account-name myprojectstorage123 \
  --resource-group my-project-rg \
  --query '[0].value' -o tsv)

# Create blob container
az storage container create \
  --name shanlee-raw-data \
  --account-name myprojectstorage123 \
  --account-key $STORAGE_KEY

# Create queue
az storage queue create \
  --name data-generation-queue \
  --account-name myprojectstorage123 \
  --account-key $STORAGE_KEY
```

#### SignalR Service

```bash
az signalr create \
  --name my-project-signalr \
  --resource-group my-project-rg \
  --location eastus \
  --sku Free_F1 \
  --unit-count 1 \
  --service-mode Default
```

Get connection string:

```bash
az signalr key list \
  --name my-project-signalr \
  --resource-group my-project-rg \
  --query primaryConnectionString -o tsv
```

## Database Setup

### 1. Connect to MySQL

```bash
mysql -h my-project-mysql.mysql.database.azure.com \
  -u adminuser \
  -p \
  --ssl-mode=REQUIRED
```

### 2. Create Database and Tables

```sql
CREATE DATABASE IF NOT EXISTS my_project_db;
USE my_project_db;

-- Application users table
CREATE TABLE app_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_user_id (user_id)
);

-- Generated data tables
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255),
    real_name VARCHAR(255),
    phone_number VARCHAR(50),
    sex VARCHAR(10),
    job VARCHAR(255),
    company VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    birth_of_date DATE,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_created_at (created_at)
);

CREATE TABLE addresses (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    title VARCHAR(255),
    address_line TEXT,
    country VARCHAR(100),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE categories (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_created_at (created_at)
);

CREATE TABLE sub_categories (
    id VARCHAR(255) PRIMARY KEY,
    parent_id VARCHAR(255),
    name VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (parent_id) REFERENCES categories(id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE products (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    category_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (category_id) REFERENCES sub_categories(id),
    INDEX idx_category_id (category_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE products_skus (
    id VARCHAR(255) PRIMARY KEY,
    product_id VARCHAR(255),
    price DECIMAL(10, 2),
    stock INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_product_id (product_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE payment_details (
    id VARCHAR(255) PRIMARY KEY,
    amount DECIMAL(10, 2),
    provider VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
);

CREATE TABLE order_details (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    payment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (payment_id) REFERENCES payment_details(id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE order_item (
    id VARCHAR(255) PRIMARY KEY,
    order_id VARCHAR(255),
    products_sku_id VARCHAR(255),
    quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES order_details(id),
    FOREIGN KEY (products_sku_id) REFERENCES products_skus(id),
    INDEX idx_order_id (order_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE wishlist (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    products_sku_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (products_sku_id) REFERENCES products_skus(id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE cart (
    id VARCHAR(255) PRIMARY KEY,
    order_id VARCHAR(255),
    products_sku_id VARCHAR(255),
    quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES order_details(id),
    FOREIGN KEY (products_sku_id) REFERENCES products_skus(id),
    INDEX idx_order_id (order_id),
    INDEX idx_created_at (created_at)
);
```

## Backend Deployment

### Option 1: Azure App Service

#### 1. Create App Service Plan

```bash
az appservice plan create \
  --name my-project-plan \
  --resource-group my-project-rg \
  --sku B1 \
  --is-linux
```

#### 2. Create Web App

```bash
az webapp create \
  --resource-group my-project-rg \
  --plan my-project-plan \
  --name my-project-backend \
  --runtime "PYTHON:3.9"
```

#### 3. Configure Environment Variables

```bash
az webapp config appsettings set \
  --resource-group my-project-rg \
  --name my-project-backend \
  --settings \
    DB_HOST="my-project-mysql.mysql.database.azure.com" \
    DB_PORT="3306" \
    DB_USER="adminuser" \
    DB_PASSWORD="<password>" \
    DB_NAME="my_project_db" \
    JWT_SECRET_KEY="<strong-secret-key>" \
    JWT_ACCESS_TOKEN_EXPIRES="900" \
    JWT_REFRESH_TOKEN_EXPIRES_DAYS="7" \
    AZURE_STORAGE_CONNECTION_STRING="<connection-string>" \
    PROXY_HOST="127.0.0.1" \
    PROXY_PORT="7890"
```

#### 4. Deploy Code

```bash
cd backend
zip -r backend.zip .
az webapp deployment source config-zip \
  --resource-group my-project-rg \
  --name my-project-backend \
  --src backend.zip
```

#### 5. Configure Startup Command

```bash
az webapp config set \
  --resource-group my-project-rg \
  --name my-project-backend \
  --startup-file "gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app"
```

Add `gunicorn` to `requirements.txt`:

```txt
gunicorn==20.1.0
```

### Option 2: Container Deployment

#### 1. Create Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "app:app"]
```

#### 2. Build and Push

```bash
cd backend

# Build image
docker build -t my-project-backend .

# Tag for Azure Container Registry
docker tag my-project-backend myregistry.azurecr.io/my-project-backend:latest

# Push to ACR
az acr login --name myregistry
docker push myregistry.azurecr.io/my-project-backend:latest
```

#### 3. Deploy to App Service

```bash
az webapp create \
  --resource-group my-project-rg \
  --plan my-project-plan \
  --name my-project-backend \
  --deployment-container-image-name myregistry.azurecr.io/my-project-backend:latest
```

## Frontend Deployment

### Option 1: Azure Static Web Apps

#### 1. Build Production Bundle

```bash
cd frontend
npm run build
```

#### 2. Deploy to Azure Static Web Apps

Using Azure CLI:

```bash
az staticwebapp create \
  --name my-project-frontend \
  --resource-group my-project-rg \
  --source . \
  --location "eastus2" \
  --branch main \
  --app-location "/frontend" \
  --output-location "dist"
```

Or use the Azure Static Web Apps CLI:

```bash
npm install -g @azure/static-web-apps-cli
swa deploy ./dist \
  --deployment-token <deployment-token>
```

#### 3. Configure API Base URL

Update frontend configuration to use production backend URL:

`frontend/src/config/api.js`:

```javascript
export const API_BASE_URL = 'https://my-project-backend.azurewebsites.net';
```

Rebuild and redeploy after changes.

### Option 2: Azure Blob Storage Static Website

#### 1. Enable Static Website

```bash
az storage blob service-properties update \
  --account-name myprojectstorage123 \
  --static-website \
  --404-document index.html \
  --index-document index.html
```

#### 2. Upload Build Files

```bash
cd frontend
npm run build

az storage blob upload-batch \
  --account-name myprojectstorage123 \
  --source ./dist \
  --destination '$web'
```

#### 3. Get Website URL

```bash
az storage account show \
  --name myprojectstorage123 \
  --resource-group my-project-rg \
  --query "primaryEndpoints.web" \
  --output tsv
```

## Azure Functions Deployment

### 1. Create Function App

```bash
az functionapp create \
  --resource-group my-project-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name my-project-functions \
  --storage-account myprojectstorage123
```

### 2. Configure Function App Settings

```bash
az functionapp config appsettings set \
  --name my-project-functions \
  --resource-group my-project-rg \
  --settings \
    AzureWebJobsStorage="<storage-connection-string>" \
    AZURE_SIGNALR_CONNECTION_STRING="<signalr-connection-string>" \
    FUNCTIONS_WORKER_RUNTIME="python"
```

### 3. Deploy Function Code

Using Azure Functions Core Tools:

```bash
cd backend/myfunc
func azure functionapp publish my-project-functions
```

Or using VS Code:
1. Install Azure Functions extension
2. Sign in to Azure
3. Right-click function app in Azure pane
4. Select "Deploy to Function App"

### 4. Verify Deployment

```bash
# List functions
az functionapp function list \
  --name my-project-functions \
  --resource-group my-project-rg

# View logs
az functionapp log tail \
  --name my-project-functions \
  --resource-group my-project-rg
```

## Environment Configuration

### Production Environment Variables

Create a secure configuration for production:

**Backend (.env):**
```env
DB_HOST=my-project-mysql.mysql.database.azure.com
DB_PORT=3306
DB_USER=adminuser
DB_PASSWORD=<secure-password>
DB_NAME=my_project_db
JWT_SECRET_KEY=<64-character-random-string>
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7
AZURE_STORAGE_CONNECTION_STRING=<azure-storage-connection>
AZURE_SIGNALR_CONNECTION_STRING=<azure-signalr-connection>
```

**Frontend (environment config):**
```javascript
export const config = {
  apiBaseUrl: 'https://my-project-backend.azurewebsites.net',
  signalRUrl: 'https://my-project-functions.azurewebsites.net/api/negotiate'
};
```

## Post-Deployment

### 1. Enable HTTPS

Azure services enable HTTPS by default. Ensure HTTP traffic redirects to HTTPS:

```bash
az webapp update \
  --resource-group my-project-rg \
  --name my-project-backend \
  --https-only true
```

### 2. Configure Custom Domain (Optional)

```bash
az webapp config hostname add \
  --webapp-name my-project-backend \
  --resource-group my-project-rg \
  --hostname api.yourdomain.com
```

### 3. Configure CORS

```bash
az webapp cors add \
  --resource-group my-project-rg \
  --name my-project-backend \
  --allowed-origins https://yourdomain.com
```

### 4. Enable Application Insights

```bash
az monitor app-insights component create \
  --app my-project-insights \
  --location eastus \
  --resource-group my-project-rg

# Link to web app
az webapp config appsettings set \
  --resource-group my-project-rg \
  --name my-project-backend \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=<key>
```

## Monitoring

### Azure Application Insights

Monitor application performance, errors, and usage:

- **Performance**: Response times, dependency durations
- **Failures**: Exception tracking, failed requests
- **Usage**: User sessions, page views
- **Custom Metrics**: Log custom events

### Log Streaming

Stream logs in real-time:

```bash
# Backend logs
az webapp log tail \
  --name my-project-backend \
  --resource-group my-project-rg

# Function logs
az functionapp log tail \
  --name my-project-functions \
  --resource-group my-project-rg
```

### Azure Monitor Alerts

Set up alerts for critical issues:

```bash
az monitor metrics alert create \
  --name high-cpu-alert \
  --resource-group my-project-rg \
  --scopes /subscriptions/<sub-id>/resourceGroups/my-project-rg/providers/Microsoft.Web/sites/my-project-backend \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m
```

## Troubleshooting

### Backend Issues

**Database Connection Errors:**
- Verify firewall rules allow connections from App Service
- Check connection string format
- Enable SSL for MySQL connections

**Import Errors:**
- Ensure all dependencies in requirements.txt
- Check Python version compatibility
- Verify startup command includes correct module path

### Frontend Issues

**API Connection Failed:**
- Verify CORS configuration on backend
- Check API base URL in frontend config
- Ensure backend is running and accessible

### Function Issues

**Queue Not Triggering:**
- Verify AzureWebJobsStorage connection string
- Check queue name matches configuration
- Review function logs for errors

**Out of Memory:**
- Reduce batch size in data generation
- Increase function memory allocation
- Optimize data generation code

### General Tips

1. **Check Application Logs**: Always start with logs
2. **Test Locally**: Replicate production config locally
3. **Use Health Checks**: Implement `/health` endpoint
4. **Monitor Resources**: Watch CPU, memory, and storage usage
5. **Backup Database**: Regular automated backups

## Rollback Procedure

If deployment fails:

1. **Backend Rollback:**
```bash
az webapp deployment slot swap \
  --resource-group my-project-rg \
  --name my-project-backend \
  --slot production
```

2. **Frontend Rollback:**
   - Redeploy previous dist folder
   - Or use version control to revert changes

3. **Function Rollback:**
   - Redeploy previous function version
   - Use deployment slots for zero-downtime

## Security Best Practices

1. **Secrets Management**: Use Azure Key Vault
2. **Network Security**: Configure virtual networks
3. **Authentication**: Enforce strong password policies
4. **SSL/TLS**: Use latest TLS version
5. **Regular Updates**: Keep dependencies updated
6. **Access Control**: Use RBAC for Azure resources

## Cost Optimization

1. Use Azure Free Tier services where possible
2. Scale down or stop non-production environments
3. Use consumption plan for Functions
4. Monitor and optimize storage usage
5. Use Azure Cost Management alerts

---

For more information, see the main [README.md](../README.md) and [API Documentation](./API.md).
