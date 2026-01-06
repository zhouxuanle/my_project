"""
ADF (Azure Data Factory) utility functions
"""
import logging
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient

logger = logging.getLogger(__name__)


def trigger_adf_pipeline(user_id: str, parent_job_id: str) -> bool:
    """
    Trigger ADF pipeline via REST API.

    Args:
        user_id: The user ID
        parent_job_id: The parent job ID

    Returns:
        bool: True if pipeline was triggered successfully, False otherwise
    """
    try:
        client = DataFactoryManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=os.environ['ADF_SUBSCRIPTION_ID']
        )

        parameters = {
            'user_id': user_id,
            'parent_job_id': parent_job_id,
            'entity_types': ["user", "address", "product", "category", "subcategory", "order", "order_item", "payment", "products_sku", "wishlist"]
        }

        response = client.pipelines.create_run(
            resource_group_name=os.environ['ADF_RESOURCE_GROUP'],
            factory_name=os.environ['ADF_FACTORY_NAME'],
            pipeline_name=os.environ['ADF_PIPELINE_NAME'],
            parameters=parameters
        )

        logger.info(f"ADF pipeline triggered for {parent_job_id}: {response.run_id}")
        return True

    except Exception as e:
        logger.error(f"Error triggering ADF pipeline: {str(e)}")
        return False