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
import sys
import traceback

# Add directories to path for imports
sys.path.append(os.path.dirname(__file__))  # functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # backend

from azure.storage.blob import BlobServiceClient
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
    @app.generic_output_binding(arg_name="signalR", type="signalR", hubName="shanleeSignalR", 
                                connectionStringSetting="AZURE_SIGNALR_CONNECTION_STRING")
    def transform_small_batch_queue(azqueue: func.QueueMessage, signalR: func.Out[str]):
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
            job_id = message.get('jobId')
            parent_job_id = message.get('parentJobId')
            
            logger.info(f"Processing small batch: job_id={job_id}, user_id={user_id}")
            transformer = PandasTransformer()
            
            # Read raw data from Bronze layer (shanlee-raw-data)
            try:
                blob_conn_str = os.environ.get('AzureWebJobsStorage')
                blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
                container_name = 'shanlee-raw-data'  
                blob_name = f'{user_id}/{parent_job_id}/{job_id}.json'  
                
                blob_client = blob_service_client.get_blob_client(
                    container=container_name,
                    blob=blob_name
                )
                download_stream = blob_client.download_blob()
                raw_data_str = download_stream.readall().decode('utf-8')
            
            except Exception as e:
                logger.error(f"Failed to read raw data from blob: {str(e)}")
                raise
            
            # Transform Bronze → Silver layer (Cleaning & Standardization)
            try:
                silver_dataframes = transformer.transform_to_silver(raw_data_str)
            except Exception as e:
                logger.error(f"Failed Silver transformation: {str(e)}")
                raise
            # Save Silver layer to ADLS Gen2
            try:
                adls_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
                for entity_type, entity_df in silver_dataframes.items():
                    parquet_bytes = entity_df.to_parquet(index=False, compression='snappy')
                    silver_file_path = f'temp/pandas/{user_id}/{parent_job_id}/{job_id}/{entity_type}.parquet'
                    silver_blob_client = adls_service_client.get_blob_client(
                        container='shanlee-cleaned-data',  
                        blob=silver_file_path
                    )
                    silver_blob_client.upload_blob(parquet_bytes, overwrite=True)
                    
                    logger.info(f"Saved {len(entity_df)} {entity_type} records to {silver_file_path}")
                
            except Exception as e:
                logger.error(f"Failed to save to ADLS Gen2: {str(e)}")
                raise
            
            # Track completion using shared helper
            try:
                tracker = JobTracker(os.environ['AzureWebJobsStorage'])
                tracker.mark_job_completed(parent_job_id, job_id)
                total_jobs = message.get('total_jobs')  
                if tracker.is_all_jobs_completed(parent_job_id, total_jobs):
                    trigger_adf_pipeline(user_id, parent_job_id)
                    log_msg = f'All data cleaning jobs completed for parent job {parent_job_id}. Merging in progress.'
                    signalR.set(json.dumps({
                        'target': 'JobStatusUpdate',
                        'arguments': [{
                            "jobId": parent_job_id,
                            "status": "completed",
                            "message": log_msg
                        }]
                    }))
                    logger.info(log_msg)
                    tracker.cleanup_completed_jobs(parent_job_id)
            except Exception as e:
                logger.error(f"Failed completion tracking: {str(e)}")
            
            logger.info(f"Small batch transformation completed successfully for job {job_id}")
            
        except Exception as e:
            logger.error(f"Error in transform_small_batch_queue: {str(e)}")
            logger.error(traceback.format_exc())
            raise


logger.info("Small batch functions registered")
