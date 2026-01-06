"""
Data Routing Logic for V1.0: Orchestrated Data Cleaning & Loading

This module handles routing of data to appropriate processing paths based on size:
- Small Batch (<=10k records): Fast Path using Pandas transformation via Azure Functions
- Large Batch (>10k records): Heavy Path using PySpark on Azure Databricks

**Medallion Architecture:**
- Bronze: Raw data container (shanlee-raw-data/) - READ ONLY SOURCE
- Silver: Cleaned data container (silver/cleaned/) - WRITE transformation output
- Gold: Analytics data container (gold/analytics/) - WRITE aggregation output
- No Bronze duplication: Raw data already exists from generation step

**Data Flow:**
1. Client submits /clean_data request with record count
2. DataRouter analyzes count and makes routing decision
3. Message queued to appropriate path (small-batch-queue or large-batch-queue)
4. ADF triggers processing:
   - Small batch: Every 10 minutes (Azure Function + Pandas)
   - Large batch: Daily at 02:00 UTC (Databricks + PySpark)
5. Processing function:
   - Reads from Bronze (shanlee-raw-data/{userId}/{jobId}.json)
    - Transforms to Silver (silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet)
    - Transforms to Gold (gold/analytics/{userId}/{parentJobId}/{jobId}/*.parquet)
6. Results loaded to Synapse + MySQL

Features:
- Determines queue destination based on data volume
- Tracks routing decisions for monitoring
- Supports direct routing based on record count
"""

import json
import base64
import logging
from azure.storage.queue import QueueClient

logger = logging.getLogger(__name__)

# Constants for routing decisions
SMALL_BATCH_THRESHOLD = 10_000  # Records

class DataRouter:
    """
    Routes data generation requests to appropriate processing queues based on volume.
    
    Implements the Decision Logic for V1.0:
    - If count <= 10k: Route to small-queue (Pandas fast path, 10-min trigger)
    - If count > 10k: Route to large-queue (Databricks heavy path, daily trigger)
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize DataRouter
        
        Args:
            connection_string: Azure Storage connection string (required).
        """
        self.connection_string = connection_string
        self.small_queue_name = 'small-batch-queue'
        self.large_queue_name = 'large-batch-queue'
        self.small_path = 'small_batch'
        self.large_path = 'large_batch'
    
    def queue_message_to_path(
        self,
        user_id: str,
        count: int,
        job_id: str,
        parent_job_id: str,
        total_jobs: int
    ) -> str:
        """
        Prepare and queue a message to the appropriate processing queue.
        
        Args:
            user_id: User ID making the request
            count: Number of records to generate
            job_id: Unique job identifier
            parent_job_id: Parent job ID for chunked processing
            total_jobs: Total number of jobs for this parent job
            
        Returns:
            Queue name where the message was sent
            
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        
        # Determine processing path and queue (only two paths supported)
        path = self.small_path if count <= SMALL_BATCH_THRESHOLD else self.large_path
        queue_name = self.small_queue_name if path == self.small_path else self.large_queue_name
        
        # Prepare message
        message = {
            'userId': user_id,
            'jobId': job_id,
            'parentJobId': parent_job_id,
            'total_jobs': total_jobs
        }
        
        encoded_message = base64.b64encode(json.dumps(message).encode('utf-8')).decode('utf-8')

        
        try:
            # Queue the message
            queue_client = QueueClient.from_connection_string(
                self.connection_string,
                queue_name
            )
            result = queue_client.send_message(encoded_message)
            
            logger.info(
                f"Message queued to {queue_name}: job_id={job_id}, "
                f"count={count}, path={path}"
            )
            
            return queue_name
            
        except Exception as e:
            logger.error(f"Failed to queue message to {queue_name}: {str(e)}")
            raise
