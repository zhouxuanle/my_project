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
- Supports both direct routing (count-based) and estimated routing (size-based)
"""

import json
import logging
from typing import Dict, Tuple
from datetime import datetime
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
        total_chunks: int = 1,
        chunk_index: int = 0
    ) -> Tuple[str, str]:
        """
        Prepare and queue a message to the appropriate processing queue.
        
        Args:
            user_id: User ID making the request
            count: Number of records to generate
            job_id: Unique job identifier
            parent_job_id: Parent job ID for chunked processing
            total_chunks: Total number of chunks in this job
            chunk_index: Current chunk index (0-based)
            
        Returns:
            Tuple of (queue_name, message_id) on success
            
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
            'count': count,
            'totalChunks': total_chunks,
            'chunkIndex': chunk_index,
            'processingPath': path,
            'timestamp': self._get_timestamp()
        }
        
        try:
            # Queue the message
            queue_client = QueueClient.from_connection_string(
                self.connection_string,
                queue_name
            )
            result = queue_client.send_message(json.dumps(message))
            
            logger.info(
                f"Message queued to {queue_name}: job_id={job_id}, "
                f"count={count}, path={path}, message_id={result['id']}"
            )
            
            return queue_name, result['id']
            
        except Exception as e:
            logger.error(f"Failed to queue message to {queue_name}: {str(e)}")
            raise
    
    def get_queue_config(self, path: str) -> Dict:
        """
        Get configuration for a specific processing path.
        
        Args:
            path: ProcessingPath enum value
            
        Returns:
            Dictionary with queue configuration
        """
        configs = {
            self.small_path: {
                'queue_name': self.small_queue_name,
                'adf_trigger_type': 'ScheduleTrigger',
                'adf_trigger_interval': 10,  # minutes
                'adf_trigger_frequency': 'Minute',
                'processor': 'Azure Function (Pandas)',
                'expected_throughput': '~5-10k records per batch',
                'max_concurrent_jobs': 10,
                'storage_account_tier': 'Standard'
            },
            self.large_path: {
                'queue_name': self.large_queue_name,
                'adf_trigger_type': 'ScheduleTrigger',
                'adf_trigger_interval': 1,  # day
                'adf_trigger_frequency': 'Day',
                'processor': 'Azure Databricks (PySpark)',
                'expected_throughput': '100k+ records per batch',
                'max_concurrent_jobs': 3,
                'storage_account_tier': 'Premium'
            }
        }
        return configs.get(path, {})
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + 'Z'
    
    @staticmethod
    def estimate_records_from_size(size_bytes: int) -> int:
        """
        Estimate number of records from blob size.
        
        Note: This is a rough estimate and may vary based on data complexity.
        
        Args:
            size_bytes: Size of the data in bytes
            
        Returns:
            Estimated record count
        """
        # Average size per complete record entry (all 11 entities)
        avg_bytes_per_record = 1024  # Rough estimate: 1KB per complete entry
        return max(1, size_bytes // avg_bytes_per_record)
