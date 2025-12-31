"""
Data Transformation Functions for V1.0: Large Batch Processing (PySpark)

This module contains Databricks notebook scripts for Silver and Gold layer transformations.
Uses PySpark for distributed processing of large datasets (>10k records).

These notebooks are executed by Azure Data Factory and run on Azure Databricks clusters.

**Medallion Architecture:**
- Bronze: Raw data container (shanlee-raw-data/) - READ ONLY SOURCE
- Silver: Cleaned data container (silver/cleaned/) - WRITE transformation output  
- Gold: Analytics data container (gold/analytics/) - WRITE aggregation output

**Data Flow for Large Batch:**
1. ADF triggers daily at 02:00 UTC
2. Databricks reads from Bronze (shanlee-raw-data/{userId}/{jobId}.json)
3. Distributed transformation to Silver (PySpark DataFrame operations)
4. Writes to Silver (silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet)
5. Distributed transformation to Gold (dimensional modeling, aggregations)
6. Writes to Gold (gold/analytics/{userId}/{parentJobId}/{jobId}/*.parquet)
7. Bulk load to Synapse + MySQL

Transformations:
- Silver Layer: Distributed data cleaning, deduplication, standardization
- Gold Layer: Distributed aggregations, dimensional modeling, business analytics
"""

# This file serves as documentation and template for Databricks notebooks
# The actual execution happens in Databricks environment

BRONZE_TO_SILVER_NOTEBOOK = """
# Databricks notebook source
# V1.0 Large Batch Transformation: Bronze → Silver Layer
# **Data Flow:** Read Bronze → Transform → Write Silver
# Executed by: Azure Data Factory (LargeBatchCleaningPipeline)
# Cluster: Standard_DS4_v2 (8 cores, distributed processing)
# Language: Python (PySpark)
# **Data Source:** Bronze layer (shanlee-raw-data/{userId}/{jobId}.json)
# **Data Destination:** Silver layer (silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet)

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging

logger = logging.getLogger(__name__)

# COMMAND ----------

# Initialize Spark Session
spark = SparkSession.builder \\
    .appName("BronzeToSilverTransformation") \\
    .getOrCreate()

# COMMAND ----------

# Read raw data from Bronze layer (ADLS Gen2 - shanlee-raw-data)
bronze_path = (
    f"/mnt/datalake/bronze/raw/"
    f"{dbutils.widgets.get('userId')}/"
    f"{dbutils.widgets.get('parentJobId')}/"
    f"{dbutils.widgets.get('jobId')}.json"
)
raw_df = spark.read.json(bronze_path)

print(f"Bronze layer records read: {raw_df.count()}")

# COMMAND ----------

# Define schema for Silver layer output
def get_silver_schema():
    return StructType([
        StructField("user_id", StringType(), True),
        StructField("username", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("user_created_at", TimestampType(), True),
        StructField("address_id", StringType(), True),
        StructField("city", StringType(), True),
        StructField("country", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("product_name", StringType(), True),
        StructField("order_id", StringType(), True),
        StructField("order_created_at", TimestampType(), True),
        StructField("quality_score", DoubleType(), True),
        StructField("processing_timestamp", TimestampType(), True)
    ])

# COMMAND ----------

# Flatten nested JSON structure
flattened_df = raw_df.select(
    col("user.id").alias("user_id"),
    col("user.username").alias("username"),
    col("user.email").alias("email"),
    col("user.phone_number").alias("phone"),
    col("user.age").alias("age"),
    col("user.create_time").cast(TimestampType()).alias("user_created_at"),
    col("address.id").alias("address_id"),
    col("address.city").alias("city"),
    col("address.country").alias("country"),
    col("product.id").alias("product_id"),
    col("product.name").alias("product_name"),
    col("order.id").alias("order_id"),
    col("order.create_time").cast(TimestampType()).alias("order_created_at")
)

# COMMAND ----------

# Data Cleaning Functions

# 1. Standardize email addresses
cleaned_df = flattened_df \\
    .withColumn("email", lower(trim(col("email")))) \\
    .filter(col("email").rlike("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\.[a-zA-Z]{2,}$"))

# 2. Standardize phone numbers (remove non-digits)
cleaned_df = cleaned_df \\
    .withColumn("phone", regexp_replace(col("phone"), "[^0-9+]", ""))

# 3. Validate age (13-120 years old)
cleaned_df = cleaned_df \\
    .withColumn("age", col("age").cast(IntegerType())) \\
    .filter((col("age") >= 13) & (col("age") <= 120))

# 4. Standardize location data
cleaned_df = cleaned_df \\
    .withColumn("city", initcap(col("city"))) \\
    .withColumn("country", upper(col("country")))

# 5. Handle null values
cleaned_df = cleaned_df \\
    .fillna("UNKNOWN", subset=["city", "country"]) \\
    .fillna(0, subset=["age"])

# COMMAND ----------

# Calculate Data Quality Score (0-100)
quality_score_df = cleaned_df \\
    .withColumn("quality_score",
        when(col("email").isNull(), 0).otherwise(100) +
        when(col("phone").isNull(), 0).otherwise(15) +
        when(col("age").isNull(), 0).otherwise(10) -
        when(col("age") < 13, 20).otherwise(0)
    ) \\
    .withColumn("quality_score", when(col("quality_score") > 100, 100)
                                  .otherwise(when(col("quality_score") < 0, 0)
                                            .otherwise(col("quality_score")))) \\
    .withColumn("processing_timestamp", current_timestamp())

# COMMAND ----------

# Remove Duplicates (keep first occurrence)
silver_df = quality_score_df \\
    .dropDuplicates(["user_id"]) \\
    .dropDuplicates(["order_id"])

print(f"Silver layer records after deduplication: {silver_df.count()}")

# COMMAND ----------

# Write Silver layer to ADLS Gen2 (Parquet format with snappy compression)
silver_path = (
    f"/mnt/datalake/silver/cleaned/"
    f"{dbutils.widgets.get('userId')}/"
    f"{dbutils.widgets.get('parentJobId')}/"
    f"{dbutils.widgets.get('jobId')}"
)
silver_df.coalesce(4) \\
    .write \\
    .mode("overwrite") \\
    .option("compression", "snappy") \\
    .parquet(silver_path)

print(f"Silver data written to {silver_path}")

# COMMAND ----------

# Log transformation metrics
metrics = {
    "bronze_records": raw_df.count(),
    "silver_records": silver_df.count(),
    "records_removed": raw_df.count() - silver_df.count(),
    "average_quality_score": silver_df.agg(avg("quality_score")).collect()[0][0],
    "transformation_date": dbutils.widgets.get("run_date")
}

spark.createDataFrame([metrics]) \\
    .coalesce(1) \\
    .write \\
    .mode("append") \\
    .option("path", "/mnt/datalake/logs/transformation_metrics") \\
    .parquet("/mnt/datalake/logs/transformation_metrics")

print("Transformation metrics logged")

# COMMAND ----------

print("Bronze → Silver transformation completed successfully!")
"""

# COMMAND ----------

SILVER_TO_GOLD_NOTEBOOK = """
# Databricks notebook source
# V1.0 Large Batch Transformation: Silver → Gold Layer
# Executed by: Azure Data Factory
# Cluster: Standard_DS4_v2 (8 cores)
# Language: Python (PySpark)

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging

logger = logging.getLogger(__name__)

# COMMAND ----------

# Initialize Spark Session
spark = SparkSession.builder \\
    .appName("SilverToGoldTransformation") \\
    .getOrCreate()

# COMMAND ----------

# Read Silver layer data
silver_path = (
    f"/mnt/datalake/silver/cleaned/"
    f"{dbutils.widgets.get('userId')}/"
    f"{dbutils.widgets.get('parentJobId')}/"
    f"{dbutils.widgets.get('jobId')}"
)
silver_df = spark.read.parquet(silver_path)

print(f"Silver layer records: {silver_df.count()}")

# COMMAND ----------

# ===== CREATE DIMENSION TABLES =====

# 1. Create dim_users (User Dimension)
dim_users = silver_df \\
    .select("user_id", "username", "email", "age", "user_created_at") \\
    .distinct() \\
    .withColumn("age_group", 
        when(col("age") < 18, "<18")
        .when(col("age") < 25, "18-24")
        .when(col("age") < 35, "25-34")
        .when(col("age") < 50, "35-49")
        .when(col("age") < 65, "50-64")
        .otherwise("65+")
    ) \\
    .withColumn("user_key", row_number().over(Window.orderBy("user_id")))

dim_users.show(10)

# COMMAND ----------

# 2. Create dim_location (Location Dimension)
dim_location = silver_df \\
    .select("city", "country") \\
    .distinct() \\
    .na.fill("UNKNOWN") \\
    .withColumn("location_key", row_number().over(Window.orderBy("country", "city")))

dim_location.show(10)

# COMMAND ----------

# 3. Create dim_time (Time Dimension for last 365 days)
time_range = spark.range(0, 365).select(
    date_sub(current_date(), col("id")).alias("date")
)

dim_time = time_range \\
    .withColumn("date_id", date_format(col("date"), "yyyyMMdd")) \\
    .withColumn("year", year(col("date"))) \\
    .withColumn("month", month(col("date"))) \\
    .withColumn("day_of_month", dayofmonth(col("date"))) \\
    .withColumn("day_of_week", dayofweek(col("date"))) \\
    .withColumn("quarter", quarter(col("date"))) \\
    .withColumn("week_of_year", weekofyear(col("date")))

dim_time.show(10)

# COMMAND ----------

# ===== CREATE FACT TABLES =====

# 4. Create fact_orders (Order Facts)
fact_orders = silver_df \\
    .groupBy("order_id", "user_id") \\
    .agg(
        first("order_created_at").alias("order_date"),
        first("product_name").alias("product_name"),
        count("product_id").alias("item_count")
    ) \\
    .withColumn("order_key", row_number().over(Window.orderBy("order_id")))

fact_orders.show(10)

# COMMAND ----------

# ===== CREATE AGGREGATE TABLES =====

# 5. Create agg_user_metrics (User Analytics)
agg_user_metrics = silver_df \\
    .groupBy("user_id") \\
    .agg(
        first("username").alias("username"),
        first("email").alias("email"),
        first("age").alias("age"),
        first("age_group").alias("age_group"),
        count("order_id").alias("total_orders"),
        count(distinct("product_id").alias("unique_products"),
        avg("quality_score").alias("avg_quality_score"),
        max("user_created_at").alias("last_updated")
    ) \\
    .withColumn("customer_segment",
        when(col("total_orders") == 0, "New")
        .when(col("total_orders") < 5, "Regular")
        .otherwise("VIP")
    )

agg_user_metrics.show(10)

# COMMAND ----------

# 6. Create agg_product_metrics (Product Analytics)
agg_product_metrics = silver_df \\
    .groupBy("product_id", "product_name") \\
    .agg(
        count("order_id").alias("times_ordered"),
        count(distinct("user_id")).alias("unique_customers"),
        avg("quality_score").alias("avg_quality_score")
    ) \\
    .orderBy(desc("times_ordered"))

agg_product_metrics.show(10)

# COMMAND ----------

# Write all Gold layer tables to ADLS Gen2

gold_base_path = (
    f"/mnt/datalake/gold/analytics/"
    f"{dbutils.widgets.get('userId')}/"
    f"{dbutils.widgets.get('parentJobId')}/"
    f"{dbutils.widgets.get('jobId')}"
)

# Write dimension tables
dim_users.coalesce(2).write.mode("overwrite").parquet(f"{gold_base_path}/dim_users")
dim_location.coalesce(2).write.mode("overwrite").parquet(f"{gold_base_path}/dim_location")
dim_time.coalesce(2).write.mode("overwrite").parquet(f"{gold_base_path}/dim_time")

# Write fact tables
fact_orders.coalesce(4).write.mode("overwrite").parquet(f"{gold_base_path}/fact_orders")

# Write aggregate tables
agg_user_metrics.coalesce(4).write.mode("overwrite").parquet(f"{gold_base_path}/agg_user_metrics")
agg_product_metrics.coalesce(2).write.mode("overwrite").parquet(f"{gold_base_path}/agg_product_metrics")

print(f"Gold layer tables written to {gold_base_path}")

# COMMAND ----------

# Log transformation metrics
metrics_dict = [{
    "gold_dim_users": dim_users.count(),
    "gold_dim_location": dim_location.count(),
    "gold_dim_time": dim_time.count(),
    "gold_fact_orders": fact_orders.count(),
    "gold_agg_user_metrics": agg_user_metrics.count(),
    "gold_agg_product_metrics": agg_product_metrics.count(),
    "transformation_date": dbutils.widgets.get("run_date")
}]

spark.createDataFrame(metrics_dict) \\
    .write \\
    .mode("append") \\
    .parquet("/mnt/datalake/logs/gold_metrics")

print("Transformation metrics logged")

# COMMAND ----------

print("Silver → Gold transformation completed successfully!")
"""


# Documentation for how to deploy these notebooks
DEPLOYMENT_INSTRUCTIONS = """
# Databricks Notebook Deployment Instructions

## Step 1: Create Workspace Folders
1. In Databricks workspace, create folders:
   - /Shared/Notebooks/
   - /Shared/Jobs/

## Step 2: Import Notebooks
1. In Databricks portal, go to Workspace
2. Create new notebook:
   - Name: bronze_to_silver_pyspark
   - Language: Python
   - Copy content from BRONZE_TO_SILVER_NOTEBOOK above
3. Create new notebook:
   - Name: silver_to_gold_pyspark
   - Language: Python
   - Copy content from SILVER_TO_GOLD_NOTEBOOK above

## Step 3: Configure ADLS Gen2 Mount
In a new notebook cell, run:
```python
configs = {
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": "<APPLICATION_ID>",
    "fs.azure.account.oauth2.client.secret": "<APPLICATION_SECRET>",
    "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token"
}

dbutils.fs.mount(
    source="abfss://datalake@<STORAGE_ACCOUNT>.dfs.core.windows.net/",
    mount_point="/mnt/datalake",
    extra_configs=configs
)
```

## Step 4: Link to Azure Data Factory
In ADF, create:
1. Activity: Databricks Notebook Activity
2. Configuration:
   - Notebook path: /Shared/Notebooks/bronze_to_silver_pyspark
   - Cluster: Standard_DS4_v2
   - Notebook parameters: {"run_date": "@{pipeline().parameters.runDate}"}

## Step 5: Test Execution
1. Manually trigger pipeline with test data
2. Monitor notebook execution in Databricks
3. Verify output in ADLS Gen2 /mnt/datalake/gold/
"""
