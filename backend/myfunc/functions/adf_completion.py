"""
Azure Function for ADF Pipeline Completion Notification

This function sends SignalR notifications when the ADF DataMergingPipeline completes.

Trigger: HTTP POST from ADF Web Activity
"""

import azure.functions as func
import json
import logging
import os

from notification_storage import NotificationStorage

logger = logging.getLogger(__name__)


def register_adf_completion_functions(app: func.FunctionApp):
    """
    Register ADF completion notification functions to the main app.
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.route(route="adf-completion", methods=["POST"])
    @app.generic_output_binding(arg_name="signalR", type="signalR", hubName="shanleeSignalR", 
                                connectionStringSetting="AZURE_SIGNALR_CONNECTION_STRING")
    def notify_adf_completion(req: func.HttpRequest, signalR: func.Out[str]):
        """
        Send SignalR notification when ADF pipeline completes successfully.
        
        Called by ADF Web Activity after DataMergingPipeline finishes.
        """
        try:
            req_body = req.get_json()
            user_id = req_body.get('user_id')
            parent_job_id = req_body.get('parent_job_id')
            
            if not user_id or not parent_job_id:
                return func.HttpResponse("Missing user_id or parent_job_id", status_code=400)
            
            log_msg = f'All data cleaning and merging jobs completed for parent job {parent_job_id}.'
            notification_id = None
            try:
                conn_str = os.environ.get('AzureWebJobsStorage')
                notification_storage = NotificationStorage(conn_str)
                notification_id = notification_storage.save_notification(
                    user_id=user_id,
                    message=log_msg,
                    status='completed'
                )
            except Exception as notif_err:
                logger.error(f'Failed to save notification to storage: {str(notif_err)}')
            
            signalR.set(json.dumps({
                'target': 'JobStatusUpdate',
                'arguments': [{
                    "id": notification_id,
                    "status": "completed",
                    "message": log_msg
                }]
            }))
            
            logger.info(log_msg)
            return func.HttpResponse("Notification sent", status_code=200)
        
        except Exception as e:
            logger.error(f"Error in notify_adf_completion: {str(e)}")
            return func.HttpResponse("Error", status_code=500)


logger.info("ADF completion functions registered")