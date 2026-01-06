import logging
import time
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError, HttpResponseError
from azure.core import MatchConditions

logger = logging.getLogger(__name__)

class JobTracker:
    def __init__(self, connection_string: str, table_name: str = 'JobCompletionStatus'):
        self.table_service_client = TableServiceClient.from_connection_string(connection_string)
        self.table_client = self.table_service_client.get_table_client(table_name)
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Create the table if it doesn't exist."""
        try:
            self.table_service_client.create_table(table_name=self.table_client.table_name)
            logger.info(f"Created table {self.table_client.table_name}")
        except ResourceExistsError:
            logger.info(f"Table {self.table_client.table_name} already exists")
        except Exception as e:
            logger.error(f"Failed to create table {self.table_client.table_name}: {str(e)}")
            raise

    def mark_job_completed(self, parent_job_id: str, job_id: str) -> None:
        """Mark a specific job as completed."""
        entity = {
            'PartitionKey': parent_job_id,
            'RowKey': job_id,
            'status': 'completed'
        }
        try:
            self.table_client.upsert_entity(entity)  # Simple upsert, no retries needed for single updates
            logger.info(f"Marked job {job_id} as completed for parent {parent_job_id}")
        except Exception as e:
            logger.error(f"Failed to mark job {job_id} completed: {str(e)}")
            raise

    def is_all_jobs_completed(self, parent_job_id: str, total_jobs: int) -> bool:
        """Check if all jobs are completed."""
        try:
            entities = list(self.table_client.query_entities(f"PartitionKey eq '{parent_job_id}' and status eq 'completed'"))
            completed = len(entities)
        except Exception as e:
            logger.error(f"Failed to get completed count for {parent_job_id}: {str(e)}")
            completed = 0
        return completed >= total_jobs

    def cleanup_completed_jobs(self, parent_job_id: str) -> None:
        """Delete all completed job entities for a parent job."""
        try:
            entities = list(self.table_client.query_entities(f"PartitionKey eq '{parent_job_id}' and status eq 'completed'"))
            for entity in entities:
                self.table_client.delete_entity(
                    partition_key=entity['PartitionKey'],
                    row_key=entity['RowKey']
                )
            logger.info(f"Cleaned up {len(entities)} completed job entities for parent {parent_job_id}")
        except Exception as e:
            logger.error(f"Failed to cleanup completed jobs for {parent_job_id}: {str(e)}")
            # Don't raise - cleanup failure shouldn't break the flow