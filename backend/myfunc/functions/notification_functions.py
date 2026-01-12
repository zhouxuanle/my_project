"""
Notification-related Azure Functions
"""
import azure.functions as func
import logging
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from notification_storage import NotificationStorage


def register_notification_functions(app: func.FunctionApp):
    """
    Register all notification-related functions to the main app
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.queue_trigger(arg_name="azqueue", queue_name="completion-notification-queue",
                       connection="AzureWebJobsStorage")
    @app.generic_output_binding(arg_name="signalR", type="signalR", hubName="shanleeSignalR", 
                                connectionStringSetting="AZURE_SIGNALR_CONNECTION_STRING")
    def process_completion_notification(azqueue: func.QueueMessage, signalR: func.Out[str]):
        """
        Process completion notifications from queue and send SignalR updates
        Ensures idempotency by checking for existing notifications
        """
        try:
            message = json.loads(azqueue.get_body().decode('utf-8'))
            user_id = message['user_id']
            parent_job_id = message['parent_job_id']
            log_msg = message['log_msg']
            
            # Instantiate NotificationStorage
            notification_storage = NotificationStorage(os.environ.get('AzureWebJobsStorage'))
            
            # Save persistent notification for offline users (idempotent)
            notification_id = notification_storage.save_notification(
                user_id=user_id,
                message=log_msg,
                status='completed',
                parent_job_id=parent_job_id
            )
            
            if notification_id is None:
                logging.info(f'Notification already exists for parent job {parent_job_id}')
                return
            
            # Send real-time SignalR notification for online users
            signalR.set(json.dumps({
                'target': 'JobStatusUpdate',
                'arguments': [{
                    "id": notification_id,
                    "status": "completed",
                    "message": log_msg
                }]
            }))
            
            logging.info(f'Completion notification processed for parent job {parent_job_id}')
            
        except Exception as e:
            logging.error(f'Error processing completion notification: {str(e)}')
    
    logging.info("Notification functions registered")