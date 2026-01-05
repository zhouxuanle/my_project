import logging
import time
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError, HttpResponseError
from azure.core import MatchConditions

logger = logging.getLogger(__name__)

class JobTracker:
    def __init__(self, connection_string: str, table_name: str = 'JobCompletionStatus'):
        self.table_client = TableServiceClient.from_connection_string(connection_string).get_table_client(table_name)

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

    def get_completed_count(self, parent_job_id: str) -> int:
        """Get the count of completed jobs for a parent job."""
        try:
            entities = list(self.table_client.query_entities(f"PartitionKey eq '{parent_job_id}' and status eq 'completed'"))
            return len(entities)
        except Exception as e:
            logger.error(f"Failed to get completed count for {parent_job_id}: {str(e)}")
            return 0

    def is_all_jobs_completed(self, parent_job_id: str, total_jobs: int) -> bool:
        """Check if all jobs are completed."""
        completed = self.get_completed_count(parent_job_id)
        return completed >= total_jobs