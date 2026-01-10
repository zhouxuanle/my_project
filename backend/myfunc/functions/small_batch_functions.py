"""
Azure Function for V1.0: Small Batch Transformation (Pandas-based)

This function is triggered by ADF pipeline and handles:
1. Reading raw data from blob storage
2. Transforming data through Silver layer (cleaning)
3. Writing to ADLS Gen2 as Parquet
4. Updating JobProgress tracking table

Trigger: Azure Data Factory (SmallBatchCleaningPipeline)
Schedule: Every 10 minutes
Processing Path: Small Batch (<=10k records)
"""

import azure.functions as func
import json
import logging
import os
from datetime import datetime
import sys
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from azure.storage.blob import BlobServiceClient, ContainerClient
from transformations.pandas import PandasTransformer
from .utils.job_tracking import JobTracker
from .utils.adf_utils import trigger_adf_pipeline

logger = logging.getLogger(__name__)


def register_small_batch_functions(app: func.FunctionApp):
    """
    Register small batch transformation functions to the main app.
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.queue_trigger(arg_name="azqueue", queue_name="small-batch-queue",
                       connection="AzureWebJobsStorage")
    def transform_small_batch_queue(azqueue: func.QueueMessage):
        """
        Process small batch data from queue, transform through Silver and Gold layers.
        
        **Processing Path:** Small Batch (≤10k records)
        **Processor:** Azure Function (Pandas)
        **Trigger:** ADF SmallBatchCleaningPipeline (every 10 minutes)
        
        Data Flow:
        1. Read message with job metadata from small-batch-queue
        2. Fetch raw data from Bronze layer (shanlee-raw-data/{userId}/{jobId}.json)
        3. Transform to Silver layer (clean & standardize)
        4. Save Silver as Parquet to ADLS Gen2 (silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet)
        5. Transform to Gold layer (dimensional modeling & aggregations)
        6. Save Gold as Parquet to ADLS Gen2 (gold/analytics/{userId}/{parentJobId}/{jobId}/*.parquet)
        7. Update JobProgress tracking table
        """
        try:
            # Parse message
            message = json.loads(azqueue.get_body().decode('utf-8'))
            user_id = message.get('userId')
            job_ids = message.get('jobIds', [])  # List of job IDs
            parent_job_id = message.get('parentJobId')
            
            logger.info(f"Processing small batch: job_ids={job_ids}, user_id={user_id}")
            
            # Process each job_id in the batch
            for job_id in job_ids:
                logger.info(f"Processing job_id: {job_id}")
                
                # Initialize transformer (could be shared, but for safety per job)
                transformer = PandasTransformer()
                
                # Read raw data from Bronze layer (shanlee-raw-data)
                try:
                    blob_conn_str = os.environ.get('AzureWebJobsStorage')
                    blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
                    container_name = 'shanlee-raw-data'  # Bronze layer container
                    blob_name = f'{user_id}/{parent_job_id}/{job_id}.json'  # Raw data path
                    
                    blob_client = blob_service_client.get_blob_client(
                        container=container_name,
                        blob=blob_name
                    )
                    
                    # Download blob content from Bronze layer
                    download_stream = blob_client.download_blob()
                    raw_data_str = download_stream.readall().decode('utf-8')
                
                except Exception as e:
                    logger.error(f"Failed to read raw data for job {job_id}: {str(e)}")
                    continue  # Skip this job, or raise depending on requirements
                
                # Transform Bronze → Silver layer (Cleaning & Standardization)
                try:
                    silver_dataframes = transformer.transform_to_silver(raw_data_str)
                    # Since all entity tables have the same length (equal to raw record count)
                    raw_record_count = len(list(silver_dataframes.values())[0]) 
               
                except Exception as e:
                    logger.error(f"Failed Silver transformation for job {job_id}: {str(e)}")
                    continue
                
                # Save Silver layer to ADLS Gen2
                try:
                    # Use BlobServiceClient for ADLS Gen2 (hierarchical namespace enabled)
                    adls_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
                    
                    # Save each entity DataFrame as separate Parquet file
                    for entity_type, entity_df in silver_dataframes.items():
                        # Convert DataFrame to Parquet bytes
                        parquet_bytes = entity_df.to_parquet(index=False, compression='snappy')
                        
                        # Create Silver layer file path for this entity type
                        silver_file_path = f'temp/pandas/{user_id}/{parent_job_id}/{job_id}/{entity_type}.parquet'
                        
                        # Upload to ADLS Gen2 container (filesystem)
                        silver_blob_client = adls_service_client.get_blob_client(
                            container='shanlee-cleaned-data',  # ADLS Gen2 filesystem name
                            blob=silver_file_path
                        )
                        silver_blob_client.upload_blob(parquet_bytes, overwrite=True)
                        
                        logger.info(f"Saved {len(entity_df)} {entity_type} records to {silver_file_path}")
                    
                except Exception as e:
                    logger.error(f"Failed to save to ADLS Gen2 for job {job_id}: {str(e)}")
                    continue
                
                # Track completion for this job
                try:
                    tracker = JobTracker(os.environ['AzureWebJobsStorage'], table_name='SmallBatchJobs')
                    tracker.mark_job_completed(user_id, parent_job_id, job_id)
                except Exception as e:
                    logger.error(f"Failed completion tracking for job {job_id}: {str(e)}")
            
            # After processing all jobs, check if all are completed and trigger ADF
            try:
                tracker = JobTracker(os.environ['AzureWebJobsStorage'], table_name='SmallBatchJobs')
                total_jobs = len(job_ids)
                if tracker.is_all_jobs_completed(user_id, parent_job_id, total_jobs):
                    # All jobs done: Trigger ADF
                    trigger_adf_pipeline(user_id, parent_job_id)
                    # Clean up completed job entities
                    tracker.cleanup_completed_jobs(user_id, parent_job_id)
            except Exception as e:
                logger.error(f"Failed final completion check: {str(e)}")
            
            logger.info(f"Small batch transformation completed for all jobs in batch {parent_job_id}")
            
        except Exception as e:
            logger.error(f"Error in transform_small_batch_queue: {str(e)}")
            logger.error(traceback.format_exc())
            raise


logger.info("Small batch functions registered")
