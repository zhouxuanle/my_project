"""
Azure Function for ADF Pipeline Completion Notification

This function sends SignalR notifications when the ADF DataMergingPipeline completes.

Trigger: HTTP POST from ADF Web Activity
"""

import azure.functions as func
import json
import logging
import os
import base64

from azure.storage.queue import QueueClient
from notification_storage import NotificationStorage

logger = logging.getLogger(__name__)


def register_adf_completion_functions(app: func.FunctionApp):
    """
    Register ADF completion notification functions to the main app.
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.route(route="adf-completion", methods=["POST"])
    def notify_adf_completion(req: func.HttpRequest):
        """
        Enqueue notification when ADF pipeline completes successfully.
        
        Called by ADF Web Activity after ADFPipeline finishes.
        Accepts optional queue_name and total_chunks in request body.
        """
        try:
            req_body = req.get_json()
            user_id = req_body.get('user_id')
            parent_job_id = req_body.get('parent_job_id')
            queue_name = req_body.get('queue_name', 'completion-notification-queue')  # Default if not provided
            
            if not user_id or not parent_job_id:
                return func.HttpResponse("Missing user_id or parent_job_id", status_code=400)
            
            log_msg = f'All data cleaning and merging jobs completed for parent job {parent_job_id}.'
            
            # Enqueue completion notification to specified queue
            try:
                conn_str = os.environ.get('AzureWebJobsStorage')
                queue_client = QueueClient.from_connection_string(conn_str, queue_name)
                notification_msg = {
                    "user_id": user_id,
                    "parent_job_id": parent_job_id,
                    "log_msg": log_msg
                }
                encoded_message = base64.b64encode(json.dumps(notification_msg).encode('utf-8')).decode('utf-8')
                queue_client.send_message(encoded_message)
                logger.info(f'Enqueued completion notification to {queue_name} for parent job {parent_job_id}')
            except Exception as enqueue_err:
                logger.error(f'Failed to enqueue completion notification: {str(enqueue_err)}')
            
            logger.info(log_msg)
            return func.HttpResponse("Notification enqueued", status_code=200)
        
        except Exception as e:
            logger.error(f"Error in notify_adf_completion: {str(e)}")
            return func.HttpResponse("Error", status_code=500)


logger.info("ADF completion functions registered")