"""
Azure Function for V1.0: Small Batch Transformation (Pandas-based)

This function is triggered by ADF pipeline and handles:
1. Reading raw data from blob storage
2. Transforming data through Silver layer (cleaning)
3. Writing to ADLS Gen2 as Parquet
4. Logging transformation metrics

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
from azure.storage.filedatalake import DataLakeServiceClient
from transformations.pandas import PandasTransformer, json_to_dataframe

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
        7. Log transformation metrics
        8. Update JobProgress tracking table
        """
        try:
            # Parse message
            message = json.loads(azqueue.get_body().decode('utf-8'))
            user_id = message.get('userId')
            job_id = message.get('jobId')
            parent_job_id = message.get('parentJobId')
            processing_timestamp = message.get('timestamp')
            
            logger.info(f"Processing small batch: job_id={job_id}, user_id={user_id}")
            
            # Initialize transformer
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
                
                # Parse JSON from Bronze layer
                raw_data = json_to_dataframe(raw_data_str)
                logger.info(f"Read {len(raw_data)} raw records from Bronze layer (shanlee-raw-data)")
                
            except Exception as e:
                logger.error(f"Failed to read raw data from blob: {str(e)}")
                raise
            
            # Transform Bronze → Silver layer (Cleaning & Standardization)
            try:
                silver_df, silver_metadata = transformer.transform_to_silver(raw_data)
                logger.info(f"Silver transformation complete: {silver_metadata}")
                logger.info(f"Silver layer output ready: {len(silver_df)} cleaned records")
                
            except Exception as e:
                logger.error(f"Failed Silver transformation: {str(e)}")
                raise
            
            # Save Silver layer to ADLS Gen2
            try:
                # Get date from timestamp
                run_date = datetime.fromisoformat(processing_timestamp).strftime('%Y-%m-%d')
                
                # Initialize ADLS client
                adls_conn_str = os.environ.get('AzureWebJobsStorage')
                adls_service_client = DataLakeServiceClient.from_connection_string(adls_conn_str)
                file_system = adls_service_client.get_file_system_client('datalake')
                
                # Create Silver layer file path (cleaned, standardized data)
                silver_file_path = f'silver/cleaned/{user_id}/{parent_job_id}/{job_id}.parquet'
                
                # Convert DataFrame to Parquet bytes
                parquet_bytes = silver_df.to_parquet(index=False, compression='snappy')
                
                # Upload to ADLS Silver layer
                file_client = file_system.get_file_client(silver_file_path)
                file_client.upload_data(parquet_bytes, overwrite=True)
                
                logger.info(f"Saved {len(silver_df)} Silver layer records to {silver_file_path}")
                
            except Exception as e:
                logger.error(f"Failed to save to ADLS Gen2: {str(e)}")
                raise
            
            # Log transformation metrics
            try:
                metrics = {
                    'jobId': job_id,
                    'userId': user_id,
                    'processingPath': 'small_batch',
                    'rawRecords': len(raw_data),
                    'silverRecords': len(silver_df),
                    'duplicatesRemoved': silver_metadata['duplicates_removed'],
                    'avgQualityScore': float(silver_metadata['quality_score_avg']),
                    'processingDurationSeconds': silver_metadata['processing_duration_seconds'],
                    'transformationTimestamp': silver_metadata['transformation_timestamp'],
                    'functionExecutionTime': datetime.utcnow().isoformat()
                }
                
                # Store metrics in blob for monitoring
                metrics_blob_client = blob_service_client.get_blob_client(
                    container='transformation-metrics',
                    blob=f'{run_date}/{job_id}_metrics.json'
                )
                metrics_blob_client.upload_blob(
                    json.dumps(metrics, indent=2),
                    overwrite=True
                )
                
                logger.info(f"Metrics logged: {metrics}")
                
            except Exception as e:
                logger.warning(f"Failed to log metrics (non-critical): {str(e)}")
            
            logger.info(f"Small batch transformation completed successfully for job {job_id}")
            
        except Exception as e:
            logger.error(f"Error in transform_small_batch_queue: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    
    logger.info("Small batch functions registered")
