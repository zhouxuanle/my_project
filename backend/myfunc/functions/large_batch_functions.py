"""
Azure Function for V1.0: Large Batch Daily Processing (Timer-Triggered)

This function runs daily at 02:00 UTC to process accumulated large batch messages:
1. Checks large-batch-queue for pending messages
2. If messages exist, processes each: triggers ADF LargeBatchCleaningPipeline
3. Deletes processed messages from queue
4. ADF orchestrates Databricks notebook for Bronze → Silver → Gold transformation

Trigger: Timer (daily at 02:00 UTC)
Schedule: Only when queue has messages
Processing Path: Large Batch (>10k records)
"""

import azure.functions as func
import json
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from azure.storage.queue import QueueClient
from .utils.adf_utils import trigger_adf_pipeline

logger = logging.getLogger(__name__)


def register_large_batch_functions(app: func.FunctionApp):
    """
    Register large batch trigger functions to the main app.
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.queue_trigger(arg_name="azqueue", queue_name="large-batch-queue",
                       connection="AzureWebJobsStorage")
    def process_large_batch_queue_daily(azqueue: func.QueueMessage):
        """
        Queue-triggered function to process large batch messages immediately.
        
        Triggers when a message is added to large-batch-queue.
        Checks for messages and processes all accumulated ones.
        
        **Processing Path:** Large Batch (>10k records)
        **Orchestrator:** Azure Data Factory
        **Processor:** Azure Databricks (PySpark)
        **Trigger:** Queue (immediate on message)
        
        Data Flow:
        1. Check large-batch-queue for messages
        2. If messages exist, process each: parse, trigger ADF LargeBatchCleaningPipeline
        3. Delete processed messages from queue
        4. ADF runs Databricks notebook for Bronze → Silver → Gold transformation
        """
        try:

            
            # Check queue message count
            queue_client = QueueClient.from_connection_string(
                os.environ['AzureWebJobsStorage'],
                'large-batch-queue'
            )
            properties = queue_client.get_queue_properties()
            message_count = properties.approximate_message_count
            
            if message_count == 0:
                logger.info("No messages in large-batch-queue. Skipping ADF trigger.")
                return
            
            logger.info(f"Processing {message_count} messages from large-batch-queue")
            
            # Process all messages (up to 32 per call, but since daily, should be fine)
            messages = queue_client.receive_messages(max_messages=32, visibility_timeout=300)  # 5 min timeout
            
            for msg in messages:
                try:
                    message = json.loads(msg.content.decode('utf-8'))
                    user_id = message.get('userId')
                    job_ids = message.get('jobIds', [])  # List of job IDs for the batch
                    parent_job_id = message.get('parentJobId')
                    logger.info(f"Processing large batch message: jobs {job_ids}, user {user_id}")
                    
                    # Trigger ADF pipeline for the entire batch
                    trigger_adf_pipeline(user_id, parent_job_id, 'ADF_LARGE_BATCH_PIPELINE_NAME')
                    queue_client.delete_message(msg)
                    
                except Exception as msg_e:
                    logger.error(f"Error processing message {msg.id}: {str(msg_e)}")
                    # Optionally, update visibility or handle poison messages
            
            logger.info(f"Processed {len(messages)} messages from large-batch-queue")
            
        except Exception as e:
            logger.error(f"Error in process_large_batch_queue_daily: {str(e)}")
            raise


logger.info("Large batch functions registered")