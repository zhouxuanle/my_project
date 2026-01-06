# Azure Data Factory Setup for Data Merging

## Overview
Your Azure Functions process data in parallel and save individual job results to temporary locations. ADF then merges all the files and saves consolidated results to the final Silver layer path.

## Current Data Flow

```
Raw Data → Small Batch Processing → Temp Files → ADF Merging → Consolidated Silver Files
```

### File Structure:
```
ADLS Gen2 Container: shanlee-cleaned-data
├── temp/pandas/{user_id}/{parent_job_id}/           # Source: Individual job files
│   ├── job_1/
│   │   ├── user.parquet
│   │   ├── address.parquet
│   │   └── ...
│   ├── job_2/
│   │   ├── user.parquet
│   │   └── ...
│   └── job_N/
│       ├── user.parquet
│       └── ...
└── pandas/{user_id}/{parent_job_id}/               # Sink: Final merged files
    ├── user.parquet          # ← All user data from all jobs merged
    ├── address.parquet       # ← All address data from all jobs merged
    ├── product.parquet       # ← All product data from all jobs merged
    └── ...
```

## Step 1: Create Azure Data Factory

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"**
3. Search for **"Data Factory"**
4. Click **"Create"**
5. Fill in:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Name**: `your-project-adf` (must be globally unique)
   - **Region**: Same as your other resources
   - **Version**: V2
6. Click **"Review + create"** → **"Create"**

## Step 2: Open ADF Studio

1. After creation, go to your Data Factory resource
2. Click **"Launch Studio"** (or "Open Azure Data Factory Studio")
3. This opens the visual ADF interface

## Step 3: Create Linked Services

### ADLS Gen2 Linked Service
1. In ADF Studio, click **"Manage"** (wrench icon) on left
2. Click **"Linked services"** → **"+ New"**
3. Search for **"Azure Data Lake Storage Gen2"**
4. Configure:
   - **Name**: `ADLSGen2LinkedService`
   - **Authentication method**: Account key (or Managed Identity)
   - **Account selection method**: From Azure subscription
   - **Storage account name**: Your storage account (where `shanlee-cleaned-data` container is)
5. Click **"Test connection"** → **"Create"**

## Step 4: Create Datasets

### Source Dataset (Temp Files)
1. Click **"Author"** (pencil icon) on left
2. Click **"+ New dataset"**
3. Search for **"Parquet"**
4. Configure:
   - **Name**: `TempParquetDataset`
   - **Linked service**: `ADLSGen2LinkedService`
   - **Parameters** tab: Add these parameters:
     - `user_id` (String)
     - `parent_job_id` (String)
     - `entity_type` (String)
   - **File path**:
     - **Container**: `shanlee-cleaned-data`
     - **Directory**: `temp/pandas/@{dataset().user_id}/@{dataset().parent_job_id}`
     - **File**: `@{dataset().entity_type}.parquet` (used for parameterization, ignored in wildcard)
5. Click **"OK"**

### Sink Dataset (Merged Files)
1. Click **"+ New dataset"**
2. Search for **"Parquet"** again
3. Configure:
   - **Name**: `MergedParquetDataset`
   - **Linked service**: `ADLSGen2LinkedService`
   - **Parameters** tab: Add these parameters:
     - `user_id` (String)
     - `parent_job_id` (String)
     - `entity_type` (String)
   - **File path**:
     - **Container**: `shanlee-cleaned-data`
     - **Directory**: `pandas/@{dataset().user_id}/@{dataset().parent_job_id}`
     - **File**: `@{dataset().entity_type}.parquet`
4. Click **"OK"**

## Step 5: Create the Pipeline

1. Click **"+ New pipeline"**
2. Name it: `DataMergingPipeline`
3. Click **"Parameters"** tab, add these parameters:
   - `user_id` (String)
   - `parent_job_id` (String)
   - `entity_types` (Array) - Default value: `["user", "address", "product", "category", "subcategory", "order", "order_item", "payment", "products_sku", "wishlist"]`

4. Drag **"ForEach"** activity onto canvas
5. Configure ForEach:
   - **Name**: `ForEachEntityType`
   - **Items**: `@pipeline().parameters.entity_types`
   - **Sequential**: Unchecked (parallel processing)

6. Inside ForEach, drag **"Copy data"** activity
7. Configure Copy Data:
   - **Name**: `MergeEntityData`
   - **Source**: `TempParquetDataset`
     - **Parameters**: 
       - `user_id`: `@{pipeline().parameters.user_id}`
       - `parent_job_id`: `@{pipeline().parameters.parent_job_id}`
       - `entity_type`: `@{item()}`
     - **File path type**: `Wildcard file path`
     - **Wildcard folder path**: `*/` (matches any job folder like `job_1/`, `job_2/`, etc.)
     - **Wildcard file name**: `@{item()}.parquet` (matches files like `user.parquet`, `address.parquet` based on the current entity type)
   - **Sink**: `MergedParquetDataset`
     - **Parameters**:
       - `user_id`: `@{pipeline().parameters.user_id}`
       - `parent_job_id`: `@{pipeline().parameters.parent_job_id}`
       - `entity_type`: `@{item()}`
     - **File path type**: `File path in dataset`
   - **Copy behavior**: `Merge files` (this combines all matching files)
   - **Mapping**: Click "Import schemas" to auto-map columns

**Wildcard Explanation**: 
- **What it is**: Wildcard file path allows ADF to find and process multiple files matching a pattern, instead of specifying exact file names.
- **Why we use it**: Your Azure Functions save data to separate job folders (job_1, job_2, etc.). We need to merge all files of the same type (e.g., all `user.parquet` files) from all job folders.
- **How the path works**: 
  - Base path from dataset: `temp/pandas/{user_id}/{parent_job_id}/`
  - Wildcard folder path `*/` matches any subfolder (job folders)
  - Wildcard file name `@{item()}.parquet` matches the current entity type (e.g., `user.parquet`)
  - Result: Finds `temp/pandas/{user_id}/{parent_job_id}/*/user.parquet` for all job folders

**Example**: For `user` entity type, this will find and merge:
- `temp/pandas/{user_id}/{parent_job_id}/job_1/user.parquet`
- `temp/pandas/{user_id}/{parent_job_id}/job_2/user.parquet`
- `temp/pandas/{user_id}/{parent_job_id}/job_3/user.parquet`
- etc.

8. Click **"Publish"** to save everything

## Step 6: Test the Pipeline

1. Click **"Add trigger"** → **"Trigger now"**
2. Fill in test parameters:
   - `user_id`: `test-user`
   - `parent_job_id`: `test-job-123`
   - `entity_types`: `["user", "address"]`
3. Click **"OK"** to run

## Step 7: Set Environment Variables

### For Local Development (Running Functions Locally)
Add to `backend/myfunc/local.settings.json` under `"Values"`:
```
{
  "ADF_SUBSCRIPTION_ID": "your-subscription-id",
  "ADF_RESOURCE_GROUP": "your-resource-group-name",
  "ADF_FACTORY_NAME": "your-adf-name",
  "ADF_PIPELINE_NAME": "DataMergingPipeline"
}
```
- Run `az login --use-device-code` in terminal to authenticate.
- Grant "Data Factory Contributor" role to your user account in ADF's IAM.

### For Deployed Azure Function App
In Azure Portal > your Function App > **Configuration** > **Application settings**, add:
```
ADF_SUBSCRIPTION_ID=your-subscription-id
ADF_RESOURCE_GROUP=your-resource-group-name
ADF_FACTORY_NAME=your-adf-name
ADF_PIPELINE_NAME=DataMergingPipeline
```
- Grant "Data Factory Contributor" role to the Function App's Managed Identity.

## Step 8: Grant Permissions

### For Local Development
1. Go to your Data Factory in Azure Portal
2. Click **"Access control (IAM)"**
3. Click **"+ Add"** → **"Add role assignment"**
4. **Role**: `Data Factory Contributor`
5. **Assign access to**: Your user account (search by email/name)
6. Click **"Save"**

### For Deployed Azure Function App
1. Go to your Data Factory in Azure Portal
2. Click **"Access control (IAM)"**
3. Click **"+ Add"** → **"Add role assignment"**
4. **Role**: `Data Factory Contributor`
5. **Assign access to**: Your Function App's Managed Identity
6. Click **"Save"**

## How It Works

1. **Azure Functions** process data and save to `temp/pandas/{user_id}/{parent_job_id}/{job_id}/{entity_type}.parquet`
2. **When all jobs complete**, Functions trigger this ADF pipeline
3. **ADF finds all files** matching `temp/pandas/{user_id}/{parent_job_id}/*/{entity_type}.parquet`
4. **Merges them together** and saves to `pandas/{user_id}/{parent_job_id}/{entity_type}.parquet`
5. **Result**: Clean consolidated Parquet files ready for analysis

## Testing

1. Run your data generation/cleaning process
2. Check ADLS Gen2 for temp files during processing
3. When complete, ADF will merge and create final files
4. Verify merged files in `pandas/{user_id}/{parent_job_id}/`

That's it! Your data processing pipeline is complete. 🎉
