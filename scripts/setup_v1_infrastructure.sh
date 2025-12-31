#!/bin/bash
# V1.0 Azure Infrastructure Setup Script
# This script sets up all required Azure resources for V1.0 implementation

set -e

# Configuration
RESOURCE_GROUP="rg-universalai-orchestrator"
REGION="eastus"
STORAGE_ACCOUNT="stguniversalai"
ADLS_ACCOUNT="adlsuniversalai"
CONTAINER_NAMES=("shanlee-raw-data" "transformation-metrics" "datalake")
QUEUE_NAMES=("small-batch-queue" "large-batch-queue" "data-generation-queue")
TABLE_NAMES=("JobProgress")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== V1.0 Azure Infrastructure Setup ===${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_error() {
    echo -e "${RED}[✗] $1${NC}"
}

# 1. Create Resource Group
echo -e "${YELLOW}Creating Resource Group...${NC}"
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$REGION" 2>/dev/null || echo "Resource group already exists"
print_status "Resource Group created: $RESOURCE_GROUP"

# 2. Create Storage Accounts
echo -e "${YELLOW}Creating Storage Accounts...${NC}"

# Blob Storage
az storage account create \
    --name "$STORAGE_ACCOUNT" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$REGION" \
    --sku Standard_LRS 2>/dev/null || echo "Storage account already exists"
print_status "Blob Storage Account created: $STORAGE_ACCOUNT"

# ADLS Gen2
az storage account create \
    --name "$ADLS_ACCOUNT" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$REGION" \
    --sku Standard_LRS \
    --enable-hierarchical-namespace true 2>/dev/null || echo "ADLS account already exists"
print_status "ADLS Gen2 Storage Account created: $ADLS_ACCOUNT"

# 3. Create Blob Containers
echo -e "${YELLOW}Creating Blob Containers...${NC}"

STORAGE_CONN_STR=$(az storage account show-connection-string \
    --resource-group "$RESOURCE_GROUP" \
    --name "$STORAGE_ACCOUNT" \
    --query connectionString -o tsv)

for container in "${CONTAINER_NAMES[@]}"; do
    az storage container create \
        --name "$container" \
        --connection-string "$STORAGE_CONN_STR" 2>/dev/null || echo "Container $container already exists"
    print_status "Container created: $container"
done

# 4. Create Storage Queues
echo -e "${YELLOW}Creating Storage Queues...${NC}"

for queue in "${QUEUE_NAMES[@]}"; do
    az storage queue create \
        --name "$queue" \
        --connection-string "$STORAGE_CONN_STR" 2>/dev/null || echo "Queue $queue already exists"
    print_status "Queue created: $queue"
done

# 5. Create Storage Tables
echo -e "${YELLOW}Creating Storage Tables...${NC}"

for table in "${TABLE_NAMES[@]}"; do
    az storage table create \
        --name "$table" \
        --connection-string "$STORAGE_CONN_STR" 2>/dev/null || echo "Table $table already exists"
    print_status "Table created: $table"
done

# 6. Create ADLS Containers (File Systems)
echo -e "${YELLOW}Creating ADLS Gen2 File Systems...${NC}"

ADLS_CONN_STR=$(az storage account show-connection-string \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ADLS_ACCOUNT" \
    --query connectionString -o tsv)

ADLS_FILE_SYSTEMS=("datalake")

for fs in "${ADLS_FILE_SYSTEMS[@]}"; do
    az storage container create \
        --name "$fs" \
        --connection-string "$ADLS_CONN_STR" 2>/dev/null || echo "File system $fs already exists"
    print_status "ADLS File System created: $fs"
done

# 7. Create Directory Structure in ADLS
echo -e "${YELLOW}Creating ADLS Directory Structure...${NC}"

# This would typically be done through Python SDK in actual implementation
# For now, we document the required structure
cat > adls_structure.txt << 'EOF'
/datalake
├── bronze/
│   └── raw/
│       └── {date}/
│           └── {jobId}.json
├── silver/
│   └── cleaned/
│       └── {date}/
│           └── {jobId}.parquet
├── gold/
│   └── analytics/
│       └── {date}/
│           ├── dim_users.parquet
│           ├── dim_location.parquet
│           ├── dim_time.parquet
│           ├── fact_orders.parquet
│           ├── agg_user_metrics.parquet
│           └── agg_product_metrics.parquet
└── logs/
    ├── transformation_metrics/
    └── pipeline_runs/
EOF

print_status "ADLS directory structure documented in adls_structure.txt"

# 8. Display Connection Strings for Configuration
echo -e "${YELLOW}Connection Strings for Configuration:${NC}"
echo ""
echo "Add these to your .env or Azure Key Vault:"
echo ""
echo "AZURE_STORAGE_CONNECTION_STRING=$STORAGE_CONN_STR"
echo "AZURE_DATALAKE_CONNECTION_STRING=$ADLS_CONN_STR"
echo ""

# 9. Summary
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""
echo "Created Resources:"
echo "  - Resource Group: $RESOURCE_GROUP"
echo "  - Blob Storage Account: $STORAGE_ACCOUNT"
echo "  - ADLS Gen2 Account: $ADLS_ACCOUNT"
echo "  - Containers: ${CONTAINER_NAMES[*]}"
echo "  - Queues: ${QUEUE_NAMES[*]}"
echo "  - Tables: ${TABLE_NAMES[*]}"
echo "  - ADLS File Systems: ${ADLS_FILE_SYSTEMS[*]}"
echo ""
echo "Next Steps:"
echo "  1. Create Azure Data Factory instance"
echo "  2. Create Azure Databricks workspace"
echo "  3. Configure ADF pipelines (see V1.0_IMPLEMENTATION.md)"
echo "  4. Deploy Databricks notebooks"
echo "  5. Set up LinkedServices in ADF"
echo ""
