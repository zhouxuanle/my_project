# 🎯 Azure Synapse & Power BI Integration Guide
## Multi-Destination Loading Stage Implementation

---

## 📊 Project Context
**Current Status:** Clean data stored in Parquet format on Azure ADLS Gen2 Silver Layer  
**Goal:** Process data in Azure Synapse and visualize in Power BI  
**Data Model:** E-commerce platform with 10+ tables

---

## 🗂️ Your E-Commerce Data Structure

Based on your `data_generators` folder analysis, you have the following tables:

| Table Name | Key Fields | Purpose |
|------------|-----------|---------|
| `users` | id, user_name, email, phone, age, job, company | Customer master data |
| `addresses` | id, user_id, address_line, city, country, postal_code | Customer shipping/billing addresses |
| `categories` | id, name, description | Product category hierarchy (Level 1) |
| `sub_categories` | id, parent_id, name, description | Product subcategories (Level 2) |
| `products` | id, name, description, category_id | Product master catalog |
| `products_skus` | id, product_id, price, stock | Product variants with pricing |
| `order_details` | id, user_id, payment_id | Order header information |
| `order_item` | id, order_id, products_sku_id, quantity | Order line items |
| `payment_details` | id, amount, provider, status | Payment transaction records |
| `wishlist` | id, user_id, products_sku_id | Customer wish lists |

---

## 🏗️ Architecture Overview

```
Azure ADLS Gen2 (Silver Layer - Parquet)
              ↓
    Azure Synapse Analytics
    ├── External Tables (PolyBase/COPY)
    ├── SQL Views (Business Logic)
    └── Materialized Views (Performance)
              ↓
        Power BI Desktop/Service
        ├── DirectQuery Mode (Real-time)
        └── Import Mode (Scheduled Refresh)
```

---

## 📋 Step-by-Step Implementation

### **Step 1: Set Up Azure Synapse Workspace**

#### 1.1 Create Synapse Workspace (Azure Portal)
```bash
# Using Azure CLI
az synapse workspace create \
  --name <your-synapse-workspace> \
  --resource-group <your-rg> \
  --storage-account <your-adls-account> \
  --file-system silver \
  --sql-admin-login-user sqladmin \
  --sql-admin-login-password <strong-password> \
  --location eastus
```

#### 1.2 Configure Firewall Rules
- Open Synapse Studio
- Navigate to **Manage** → **Security** → **Networking**
- Add your client IP address
- Enable "Allow Azure services and resources to access this workspace"

---

### **Step 2: Create External Data Source in Synapse**

#### 2.1 Create Master Key & Database Credential
```sql
-- Run in Synapse SQL Pool (Dedicated or Serverless)
USE [master];
GO

-- Create Master Key (one-time)
CREATE MASTER KEY ENCRYPTION BY PASSWORD = '<your-strong-password>';
GO

-- Create Database Scoped Credential for ADLS Gen2
CREATE DATABASE SCOPED CREDENTIAL ADLSCredential
WITH IDENTITY = 'Managed Identity'; -- Or use 'SHARED ACCESS SIGNATURE'
GO
```

#### 2.2 Create External Data Source
```sql
-- Create External Data Source pointing to your Silver Layer
CREATE EXTERNAL DATA SOURCE SilverLayerADLS
WITH (
    TYPE = HADOOP,
    LOCATION = 'abfss://silver@<your-storage-account>.dfs.core.windows.net/',
    CREDENTIAL = ADLSCredential
);
GO
```

#### 2.3 Create External File Format
```sql
-- Define Parquet file format
CREATE EXTERNAL FILE FORMAT ParquetFileFormat
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
GO
```

---

### **Step 3: Create External Tables**

#### 3.0 Understanding Your Silver Layer Structure

Your cleaned data is organized in this hierarchy:
```
silver/
├── pandas/
│   └── <user_id>/
│       └── <parent_job_id>/
│           ├── users.parquet
│           ├── categories.parquet
│           └── ... (other entities)
└── spark/
    └── <user_id>/
        └── <parent_job_id>/
            ├── users.parquet
            ├── categories.parquet
            └── ... (other entities)
```

**Challenge:** Sometimes only `pandas/` path exists, sometimes only `spark/`, sometimes both exist. We need to read all entity parquet files from all possible paths.

**Solution:** Use wildcard patterns in EXTERNAL TABLE LOCATION to read from multiple subdirectories dynamically.

---

#### 3.1 Create External Tables with Wildcard Patterns

```sql
-- Switch to your database
USE [eCommerce_DW];
GO

-- Users Table (reads from both pandas/ and spark/ paths with wildcards)
CREATE EXTERNAL TABLE ext_users (
    id VARCHAR(255),
    user_name VARCHAR(255),
    real_name VARCHAR(255),
    phone_number VARCHAR(255),
    sex VARCHAR(255),
    job VARCHAR(255),
    company VARCHAR(255),
    email VARCHAR(255),
    birth_of_date DATE,
    age INT,
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/users.parquet',  -- Reads: pandas/*/*/users.parquet AND spark/*/*/users.parquet
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Categories Table
CREATE EXTERNAL TABLE ext_categories (
    id VARCHAR(255),
    name VARCHAR(255),
    description VARCHAR(500),
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/categories.parquet',  -- Reads from all processing paths
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Sub Categories Table
CREATE EXTERNAL TABLE ext_sub_categories (
    id VARCHAR(255),
    parent_id VARCHAR(255),
    name VARCHAR(255),
    description VARCHAR(500),
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/sub_categories.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Products Table
CREATE EXTERNAL TABLE ext_products (
    id VARCHAR(255),
    name VARCHAR(255),
    description VARCHAR(500),
    category_id VARCHAR(255),
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/products.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Products SKUs Table
CREATE EXTERNAL TABLE ext_products_skus (
    id VARCHAR(255),
    product_id VARCHAR(255),
    price DECIMAL(18,2),
    stock INT,
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/products_skus.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Order Details Table
CREATE EXTERNAL TABLE ext_order_details (
    id VARCHAR(255),
    user_id VARCHAR(255),
    payment_id VARCHAR(255),
    created_at DATETIME2,
    updated_at DATETIME2
)
WITH (
    LOCATION = '/*/*/order_details.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Order Item Table
CREATE EXTERNAL TABLE ext_order_item (
    id VARCHAR(255),
    order_id VARCHAR(255),
    products_sku_id VARCHAR(255),
    quantity INT,
    created_at DATETIME2,
    updated_at DATETIME2
)
WITH (
    LOCATION = '/*/*/order_item.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Payment Details Table
CREATE EXTERNAL TABLE ext_payment_details (
    id VARCHAR(255),
    amount DECIMAL(18,2),
    provider VARCHAR(255),
    status VARCHAR(255),
    created_at DATETIME2,
    updated_at DATETIME2
)
WITH (
    LOCATION = '/*/*/payment_details.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Addresses Table
CREATE EXTERNAL TABLE ext_addresses (
    id VARCHAR(255),
    user_id VARCHAR(255),
    title VARCHAR(255),
    address_line VARCHAR(500),
    country VARCHAR(255),
    city VARCHAR(255),
    postal_code VARCHAR(50),
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/addresses.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO

-- Wishlist Table
CREATE EXTERNAL TABLE ext_wishlist (
    id VARCHAR(255),
    user_id VARCHAR(255),
    products_sku_id VARCHAR(255),
    created_at DATETIME2,
    deleted_at DATETIME2
)
WITH (
    LOCATION = '/*/*/wishlist.parquet',
    DATA_SOURCE = SilverLayerADLS,
    FILE_FORMAT = ParquetFileFormat
);
GO
```

---

#### 3.2 Alternative: OPENROWSET Approach (More Flexible)

If you need more control or want to query specific paths dynamically, use `OPENROWSET`:

```sql
-- Example: Query users from both pandas and spark paths
SELECT *
FROM OPENROWSET(
    BULK 'pandas/*/*/users.parquet, spark/*/*/users.parquet',
    DATA_SOURCE = 'SilverLayerADLS',
    FORMAT = 'PARQUET'
) AS users;

-- Create a VIEW using OPENROWSET (useful for dynamic paths)
CREATE VIEW vw_users_dynamic AS
SELECT *
FROM OPENROWSET(
    BULK '/*/*/users.parquet',  -- Will match: pandas/*/*/users.parquet AND spark/*/*/users.parquet
    DATA_SOURCE = 'SilverLayerADLS',
    FORMAT = 'PARQUET'
) AS users;
GO
```

---

#### 3.3 Advanced: Union Specific Paths (If Wildcard Doesn't Work)

If your Synapse version has limitations with wildcards, explicitly UNION data:

```sql
CREATE VIEW ext_users_union AS
SELECT * FROM OPENROWSET(
    BULK 'pandas/*/*/users.parquet',
    DATA_SOURCE = 'SilverLayerADLS',
    FORMAT = 'PARQUET'
) AS pandas_users
UNION ALL
SELECT * FROM OPENROWSET(
    BULK 'spark/*/*/users.parquet',
    DATA_SOURCE = 'SilverLayerADLS',
    FORMAT = 'PARQUET'
) AS spark_users;
GO
```

---

#### 3.4 Verify Your External Tables

Test that the wildcard pattern works correctly:

```sql
-- Test: Check if data is being read from both paths
SELECT 
    COUNT(*) AS total_records,
    MIN(created_at) AS earliest_record,
    MAX(created_at) AS latest_record
FROM ext_users;

-- Test: Verify all entities are accessible
SELECT 'users' AS entity, COUNT(*) AS record_count FROM ext_users
UNION ALL
SELECT 'categories', COUNT(*) FROM ext_categories
UNION ALL
SELECT 'products', COUNT(*) FROM ext_products
UNION ALL
SELECT 'order_details', COUNT(*) FROM ext_order_details
UNION ALL
SELECT 'payment_details', COUNT(*) FROM ext_payment_details;
```

---

## 🔍 Recommended Data Analytics & SQL Views

### **1. Sales Performance Dashboard**

#### View: Sales Overview
```sql
CREATE VIEW vw_sales_overview AS
SELECT 
    CAST(od.created_at AS DATE) AS order_date,
    COUNT(DISTINCT od.id) AS total_orders,
    COUNT(DISTINCT od.user_id) AS unique_customers,
    SUM(oi.quantity) AS total_items_sold,
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS total_revenue,
    AVG(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS avg_order_value,
    SUM(CASE WHEN pd.status = 'Success' THEN 1 ELSE 0 END) AS successful_payments,
    SUM(CASE WHEN pd.status = 'Failed' THEN 1 ELSE 0 END) AS failed_payments,
    SUM(CASE WHEN pd.status = 'Refunded' THEN 1 ELSE 0 END) AS refunded_payments
FROM ext_order_details od
INNER JOIN ext_order_item oi ON od.id = oi.order_id
INNER JOIN ext_products_skus ps ON oi.products_sku_id = ps.id
LEFT JOIN ext_payment_details pd ON od.payment_id = pd.id
WHERE od.deleted_at IS NULL
GROUP BY CAST(od.created_at AS DATE);
GO
```

**Power BI Visualizations:**
- Line chart: Daily revenue trend
- KPI cards: Total revenue, orders, customers
- Donut chart: Payment status distribution

---

### **2. Product Performance Analysis**

#### View: Top Selling Products
```sql
CREATE VIEW vw_product_performance AS
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    c.name AS category_name,
    sc.name AS subcategory_name,
    COUNT(DISTINCT oi.order_id) AS times_ordered,
    SUM(oi.quantity) AS total_quantity_sold,
    AVG(CAST(ps.price AS DECIMAL(18,2))) AS avg_price,
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS total_revenue,
    AVG(ps.stock) AS avg_stock_level,
    COUNT(DISTINCT w.user_id) AS wishlist_count
FROM ext_products p
INNER JOIN ext_categories c ON p.category_id = c.id
LEFT JOIN ext_sub_categories sc ON sc.parent_id = c.id
INNER JOIN ext_products_skus ps ON p.id = ps.product_id
LEFT JOIN ext_order_item oi ON ps.id = oi.products_sku_id
LEFT JOIN ext_wishlist w ON ps.id = w.products_sku_id
WHERE p.deleted_at IS NULL
GROUP BY p.id, p.name, c.name, sc.name;
GO
```

**Power BI Visualizations:**
- Bar chart: Top 10 products by revenue
- Treemap: Category distribution
- Scatter plot: Price vs quantity sold
- Table: Product details with drill-through

---

### **3. Customer Insights**

#### View: Customer Segmentation
```sql
CREATE VIEW vw_customer_insights AS
SELECT 
    u.id AS user_id,
    u.user_name,
    u.real_name,
    u.email,
    u.age,
    u.sex,
    u.job,
    u.company,
    u.phone_number,
    a.country,
    a.city,
    COUNT(DISTINCT od.id) AS total_orders,
    SUM(oi.quantity) AS total_items_purchased,
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS lifetime_value,
    AVG(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS avg_order_value,
    MAX(od.created_at) AS last_order_date,
    MIN(od.created_at) AS first_order_date,
    DATEDIFF(day, MIN(od.created_at), MAX(od.created_at)) AS customer_tenure_days,
    COUNT(DISTINCT w.id) AS wishlist_items_count,
    -- Customer Segment
    CASE 
        WHEN SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) > 10000 THEN 'VIP'
        WHEN SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) > 5000 THEN 'Premium'
        WHEN SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) > 1000 THEN 'Regular'
        ELSE 'New'
    END AS customer_segment
FROM ext_users u
LEFT JOIN ext_addresses a ON u.id = a.user_id
LEFT JOIN ext_order_details od ON u.id = od.user_id
LEFT JOIN ext_order_item oi ON od.id = oi.order_id
LEFT JOIN ext_products_skus ps ON oi.products_sku_id = ps.id
LEFT JOIN ext_wishlist w ON u.id = w.user_id
WHERE u.deleted_at IS NULL
GROUP BY 
    u.id, u.user_name, u.real_name, u.email, u.age, 
    u.sex, u.job, u.company, u.phone_number, a.country, a.city;
GO
```

**Power BI Visualizations:**
- Funnel chart: Customer segments
- Map visualization: Customer distribution by country/city
- Slicer: Age groups, job types
- Matrix: Customer lifetime value ranking

---

### **4. Inventory & Stock Management**

#### View: Inventory Status
```sql
CREATE VIEW vw_inventory_status AS
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    c.name AS category_name,
    ps.id AS sku_id,
    ps.price,
    ps.stock AS current_stock,
    ISNULL(SUM(oi.quantity), 0) AS total_sold_last_30_days,
    -- Stock status
    CASE 
        WHEN ps.stock = 0 THEN 'Out of Stock'
        WHEN ps.stock < 10 THEN 'Low Stock'
        WHEN ps.stock < 50 THEN 'Medium Stock'
        ELSE 'Well Stocked'
    END AS stock_status,
    -- Estimated days to stockout (simple calculation)
    CASE 
        WHEN ISNULL(SUM(oi.quantity), 0) = 0 THEN NULL
        ELSE ps.stock / (ISNULL(SUM(oi.quantity), 1) / 30.0)
    END AS estimated_days_to_stockout
FROM ext_products p
INNER JOIN ext_categories c ON p.category_id = c.id
INNER JOIN ext_products_skus ps ON p.id = ps.product_id
LEFT JOIN ext_order_item oi 
    ON ps.id = oi.products_sku_id 
    AND oi.created_at >= DATEADD(day, -30, GETDATE())
WHERE p.deleted_at IS NULL
GROUP BY p.id, p.name, c.name, ps.id, ps.price, ps.stock;
GO
```

**Power BI Visualizations:**
- Gauge chart: Stock status distribution
- Table with conditional formatting: Low stock alerts
- Bar chart: Products needing restock

---

### **5. Payment & Financial Analysis**

#### View: Payment Analytics
```sql
CREATE VIEW vw_payment_analytics AS
SELECT 
    pd.provider AS payment_provider,
    pd.status AS payment_status,
    COUNT(DISTINCT pd.id) AS transaction_count,
    SUM(CAST(pd.amount AS DECIMAL(18,2))) AS total_amount,
    AVG(CAST(pd.amount AS DECIMAL(18,2))) AS avg_transaction_amount,
    MIN(CAST(pd.amount AS DECIMAL(18,2))) AS min_amount,
    MAX(CAST(pd.amount AS DECIMAL(18,2))) AS max_amount,
    CAST(pd.created_at AS DATE) AS transaction_date,
    -- Success rate
    CAST(
        SUM(CASE WHEN pd.status = 'Success' THEN 1 ELSE 0 END) * 100.0 
        / COUNT(*) 
        AS DECIMAL(5,2)
    ) AS success_rate_pct
FROM ext_payment_details pd
WHERE pd.created_at IS NOT NULL
GROUP BY pd.provider, pd.status, CAST(pd.created_at AS DATE);
GO
```

**Power BI Visualizations:**
- Column chart: Payment provider comparison
- Donut chart: Success vs failed transactions
- Line chart: Payment trends over time

---

### **6. Geographic Sales Analysis**

#### View: Sales by Location
```sql
CREATE VIEW vw_sales_by_location AS
SELECT 
    a.country,
    a.city,
    a.postal_code,
    COUNT(DISTINCT u.id) AS customer_count,
    COUNT(DISTINCT od.id) AS total_orders,
    SUM(oi.quantity) AS total_items,
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS total_revenue,
    AVG(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS avg_order_value
FROM ext_addresses a
INNER JOIN ext_users u ON a.user_id = u.id
LEFT JOIN ext_order_details od ON u.id = od.user_id
LEFT JOIN ext_order_item oi ON od.id = oi.order_id
LEFT JOIN ext_products_skus ps ON oi.products_sku_id = ps.id
WHERE a.deleted_at IS NULL AND u.deleted_at IS NULL
GROUP BY a.country, a.city, a.postal_code;
GO
```

**Power BI Visualizations:**
- Filled map: Revenue by country
- Drill-through: Country → City → Postal code
- Heat map: Customer concentration

---

### **7. Category Deep Dive**

#### View: Category Performance
```sql
CREATE VIEW vw_category_performance AS
SELECT 
    c.id AS category_id,
    c.name AS category_name,
    sc.id AS subcategory_id,
    sc.name AS subcategory_name,
    COUNT(DISTINCT p.id) AS product_count,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.quantity) AS units_sold,
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS revenue,
    AVG(CAST(ps.price AS DECIMAL(18,2))) AS avg_product_price,
    -- Revenue contribution
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) * 100.0 / 
        SUM(SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity)) 
        OVER () AS revenue_percentage
FROM ext_categories c
LEFT JOIN ext_sub_categories sc ON c.id = sc.parent_id
INNER JOIN ext_products p ON c.id = p.category_id
INNER JOIN ext_products_skus ps ON p.id = ps.product_id
LEFT JOIN ext_order_item oi ON ps.id = oi.products_sku_id
WHERE c.deleted_at IS NULL
GROUP BY c.id, c.name, sc.id, sc.name;
GO
```

**Power BI Visualizations:**
- Waterfall chart: Category revenue contribution
- Clustered bar chart: Category vs Subcategory comparison
- Matrix with hierarchy: Category → Subcategory → Products

---

### **8. Cohort Analysis (Customer Retention)**

#### View: Monthly Cohort Analysis
```sql
CREATE VIEW vw_cohort_analysis AS
WITH FirstOrders AS (
    SELECT 
        user_id,
        DATEADD(month, DATEDIFF(month, 0, MIN(created_at)), 0) AS cohort_month,
        MIN(created_at) AS first_order_date
    FROM ext_order_details
    WHERE deleted_at IS NULL
    GROUP BY user_id
),
UserOrders AS (
    SELECT 
        od.user_id,
        DATEADD(month, DATEDIFF(month, 0, od.created_at), 0) AS order_month,
        COUNT(DISTINCT od.id) AS order_count,
        SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS revenue
    FROM ext_order_details od
    INNER JOIN ext_order_item oi ON od.id = oi.order_id
    INNER JOIN ext_products_skus ps ON oi.products_sku_id = ps.id
    WHERE od.deleted_at IS NULL
    GROUP BY od.user_id, DATEADD(month, DATEDIFF(month, 0, od.created_at), 0)
)
SELECT 
    fo.cohort_month,
    uo.order_month,
    DATEDIFF(month, fo.cohort_month, uo.order_month) AS months_since_first_order,
    COUNT(DISTINCT fo.user_id) AS cohort_size,
    COUNT(DISTINCT uo.user_id) AS returning_customers,
    CAST(COUNT(DISTINCT uo.user_id) * 100.0 / COUNT(DISTINCT fo.user_id) AS DECIMAL(5,2)) AS retention_rate,
    SUM(uo.revenue) AS cohort_revenue
FROM FirstOrders fo
LEFT JOIN UserOrders uo ON fo.user_id = uo.user_id
GROUP BY fo.cohort_month, uo.order_month;
GO
```

**Power BI Visualizations:**
- Cohort retention heatmap matrix
- Line chart: Retention rate over time

---

## 🎨 Power BI Connection & Setup

### **Step 4: Connect Power BI to Synapse**

#### 4.1 Power BI Desktop Connection
1. Open **Power BI Desktop**
2. Click **Get Data** → **Azure** → **Azure Synapse Analytics (SQL)**
3. Enter connection details:
   - **Server:** `<your-synapse-workspace>.sql.azuresynapse.net`
   - **Database:** `eCommerce_DW`
   - **Data Connectivity mode:** 
     - **DirectQuery** (real-time, recommended for large datasets)
     - **Import** (scheduled refresh, better performance for small datasets)

#### 4.2 Authentication
- Select **Microsoft Account** or **Service Principal**
- Sign in with your Azure credentials

#### 4.3 Select Views/Tables
- Choose the views created above (vw_sales_overview, vw_product_performance, etc.)
- Click **Load** or **Transform Data** (Power Query)

---

### **Step 5: Build Power BI Dashboard**

#### Recommended Dashboard Pages:

**Page 1: Executive Summary**
- KPI Cards: Total Revenue, Total Orders, Unique Customers
- Line Chart: Daily Revenue Trend (vw_sales_overview)
- Donut Chart: Payment Status Distribution
- Map: Sales by Country (vw_sales_by_location)

**Page 2: Product Analytics**
- Bar Chart: Top 10 Products by Revenue (vw_product_performance)
- Treemap: Category Revenue Distribution (vw_category_performance)
- Table: Product Details with Drill-through
- Slicer: Category, Subcategory

**Page 3: Customer Intelligence**
- Funnel: Customer Segments (vw_customer_insights)
- Scatter Plot: Customer Lifetime Value vs Order Count
- Matrix: Top Customers Ranked
- Slicer: Age, Sex, Job, Country

**Page 4: Inventory Management**
- Gauge: Stock Status Distribution (vw_inventory_status)
- Table with Conditional Formatting: Low Stock Alerts
- Bar Chart: Products Needing Restock
- Card: Out of Stock Count

**Page 5: Financial Performance**
- Column Chart: Payment Provider Comparison (vw_payment_analytics)
- Line Chart: Payment Trends
- KPI: Success Rate %
- Waterfall: Category Revenue Contribution (vw_category_performance)

**Page 6: Retention & Cohorts**
- Cohort Matrix Heatmap (vw_cohort_analysis)
- Line Chart: Monthly Retention Rate
- Card: Average Customer Tenure

---

## 🚀 Performance Optimization Tips

### **1. Materialized Views (For Better Performance)**
```sql
-- Example: Materialize frequently accessed aggregations
CREATE MATERIALIZED VIEW mv_daily_sales_summary
WITH (DISTRIBUTION = HASH(order_date))
AS
SELECT 
    CAST(od.created_at AS DATE) AS order_date,
    COUNT(DISTINCT od.id) AS total_orders,
    SUM(CAST(ps.price AS DECIMAL(18,2)) * oi.quantity) AS total_revenue
FROM ext_order_details od
INNER JOIN ext_order_item oi ON od.id = oi.order_id
INNER JOIN ext_products_skus ps ON oi.products_sku_id = ps.id
GROUP BY CAST(od.created_at AS DATE);
GO

-- Refresh materialized view
ALTER MATERIALIZED VIEW mv_daily_sales_summary REBUILD;
```

### **2. Indexing (For Dedicated SQL Pool)**
```sql
-- Create clustered columnstore index (default for best compression)
CREATE CLUSTERED COLUMNSTORE INDEX idx_sales
ON dbo.fact_sales;

-- Create non-clustered index for frequent filters
CREATE NONCLUSTERED INDEX idx_order_date
ON dbo.fact_sales (order_date);
```

### **3. Partitioning Strategy**
```sql
-- Partition large tables by date for better query performance
CREATE TABLE fact_sales_partitioned (
    order_id VARCHAR(255),
    order_date DATE,
    revenue DECIMAL(18,2)
)
WITH (
    DISTRIBUTION = HASH(order_id),
    PARTITION (order_date RANGE RIGHT FOR VALUES 
        ('2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01'))
);
```

---

## 📊 Power BI DAX Measures (Advanced)

Add these calculated measures in Power BI for dynamic analytics:

```dax
// Total Revenue
Total Revenue = 
SUMX(
    vw_sales_overview,
    vw_sales_overview[total_revenue]
)

// Month-over-Month Growth
MoM Revenue Growth % = 
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = 
    CALCULATE(
        [Total Revenue],
        DATEADD(vw_sales_overview[order_date], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0) * 100

// Year-to-Date Revenue
YTD Revenue = 
TOTALYTD(
    [Total Revenue],
    vw_sales_overview[order_date]
)

// Average Order Value
Avg Order Value = 
AVERAGEX(
    vw_sales_overview,
    vw_sales_overview[avg_order_value]
)

// Customer Lifetime Value
Customer LTV = 
SUMX(
    vw_customer_insights,
    vw_customer_insights[lifetime_value]
)

// Conversion Rate (Orders / Customers)
Conversion Rate % = 
DIVIDE(
    SUM(vw_sales_overview[total_orders]),
    SUM(vw_sales_overview[unique_customers]),
    0
) * 100
```

---

## 🔄 Automated Refresh Strategy

### **Option 1: Power BI Service Scheduled Refresh (Import Mode)**
1. Publish report to Power BI Service
2. Go to **Settings** → **Scheduled refresh**
3. Set refresh frequency (up to 8x/day for Pro, 48x/day for Premium)

### **Option 2: DirectQuery (Real-time)**
- No refresh needed
- Queries run directly against Synapse
- Use for real-time dashboards

### **Option 3: Hybrid (Composite Model)**
- Use **DirectQuery** for large fact tables
- Use **Import** for small dimension tables
- Best balance of performance and freshness

---

## 🛡️ Security Best Practices

### **Row-Level Security (RLS) in Synapse**
```sql
-- Create security policy for customer segmentation
CREATE SCHEMA Security;
GO

CREATE FUNCTION Security.fn_customer_security(@UserEmail VARCHAR(255))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN
    SELECT 1 AS allowed
    WHERE @UserEmail = USER_NAME() 
       OR IS_MEMBER('DataAnalyst') = 1;
GO

-- Apply security policy
CREATE SECURITY POLICY Security.CustomerSecurityPolicy
ADD FILTER PREDICATE Security.fn_customer_security(email)
ON dbo.vw_customer_insights
WITH (STATE = ON);
GO
```

### **Power BI RLS**
```dax
// Define role in Power BI
[Email] = USERPRINCIPALNAME()
```

---

## 📈 Monitoring & Troubleshooting

### **Monitor Synapse Query Performance**
```sql
-- Check running queries
SELECT 
    session_id,
    request_id,
    start_time,
    total_elapsed_time,
    command,
    status
FROM sys.dm_pdw_exec_requests
WHERE status NOT IN ('Completed', 'Failed', 'Cancelled')
ORDER BY start_time DESC;
```

### **Power BI Performance Analyzer**
- In Power BI Desktop: **View** → **Performance Analyzer**
- Identify slow visuals and optimize DAX queries

---

## 🎯 Next Steps (Gold Layer)

After validating your Silver→Synapse→Power BI pipeline, consider:

1. **Create Gold Layer (Curated Views)**
   - Pre-aggregated star schema
   - Dimension tables (dim_customer, dim_product, dim_date)
   - Fact tables (fact_sales, fact_inventory)

2. **Implement CDC (Change Data Capture)**
   - Track only changed records
   - Optimize refresh performance

3. **Add Real-time Streaming**
   - Azure Stream Analytics → Power BI
   - For live order tracking

---

## 📚 Resources & References

- [Azure Synapse Analytics Documentation](https://learn.microsoft.com/en-us/azure/synapse-analytics/)
- [Power BI Integration with Synapse](https://learn.microsoft.com/en-us/power-bi/connect-data/service-azure-sql-data-warehouse-with-direct-connect)
- [PolyBase External Tables](https://learn.microsoft.com/en-us/sql/relational-databases/polybase/polybase-guide)
- [Power BI Best Practices](https://learn.microsoft.com/en-us/power-bi/guidance/)

---

## ✅ Implementation Checklist

- [ ] Azure Synapse Workspace created
- [ ] Firewall rules configured
- [ ] External data source connected to ADLS Gen2 Silver Layer
- [ ] External tables created for all 10 data tables
- [ ] SQL views created for analytics (8 views minimum)
- [ ] Power BI Desktop installed and connected to Synapse
- [ ] Dashboard created with 6 pages (Executive, Product, Customer, Inventory, Financial, Retention)
- [ ] DAX measures implemented
- [ ] Report published to Power BI Service
- [ ] Scheduled refresh configured (if using Import mode)
- [ ] Row-level security implemented (if needed)
- [ ] Performance monitoring enabled

---

## 🎊 Summary

You now have a complete **Multi-Destination Loading** pipeline:

```
Bronze (Raw) → Silver (Cleaned Parquet) → Synapse (SQL Views) → Power BI (Visualization)
```

**Key Achievements:**
✅ 10 External tables in Synapse  
✅ 8 Pre-built analytical views  
✅ 6 Power BI dashboard pages  
✅ Real-time/Scheduled refresh capability  
✅ Ready for Gold layer (Star schema) in V2.0

**Your data is now ready for executive decision-making!** 🚀
