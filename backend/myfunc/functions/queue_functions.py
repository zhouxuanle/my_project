"""
Queue-triggered Azure Functions for data processing
"""
import azure.functions as func
import logging
import os
import json
import sys
import base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueClient
from generate_event_tracking_data import DataGenerator
from .utils.job_tracking import JobTracker


def register_queue_functions(app: func.FunctionApp):
    """
    Register all queue-triggered functions to the main app
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.queue_trigger(arg_name="azqueue", queue_name="data-generation-queue",
                       connection="AzureWebJobsStorage")
    def process_data_generation_job(azqueue: func.QueueMessage):
        """
        Process data generation jobs from queue and upload to blob storage
        Enqueues completion notifications when all chunks are done
        """
        try:
            # Parse job message
            message = json.loads(azqueue.get_body().decode('utf-8'))
            user_id = message.get('userId')
            parent_job_id = message.get('parentJobId')
            job_id = message.get('jobId')
            count = int(message.get('count', 1))
            total_chunks = int(message.get('totalChunks', 1))  # Default to 1 if not present

            # Generate data
            gd = DataGenerator()
            generated_data = []
            for _ in range(count):
                user = gd.generate_user_data()
                address = gd.generate_fake_address(user)
                category = gd.generate_categories_data()
                subcategory = gd.generate_subcategories_data(category)
                product = gd.generate_products_data(subcategory)
                products_sku = gd.generate_sku_data(category, subcategory, product)
                wishlist = gd.generate_wishlist_data(products_sku, user)
                payment = gd.generate_payment_details_data()
                order = gd.generate_order_details_data(user, payment)
                order_item = gd.generate_order_item_data(products_sku, order)
                generated_data.append({
                    "user": user,
                    "address": address,
                    "category": category,
                    "subcategory": subcategory,
                    "product": product,
                    "products_sku": products_sku,
                    "wishlist": wishlist,
                    "payment": payment,
                    "order": order,
                    "order_item": order_item
                })

            # Upload to Azure Blob Storage
            blob_conn_str = os.environ.get('AzureWebJobsStorage')
            blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
            container_name = 'shanlee-raw-data'      
            blob_name = f'{user_id}/{parent_job_id}/{job_id}.json'
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_client.upload_blob(json.dumps(generated_data, default=str), overwrite=True)

            # Mark this job as completed using JobTracker
            tracker = JobTracker(blob_conn_str, table_name='DataGenerationJobs')
            tracker.mark_job_completed(user_id, parent_job_id, job_id)

            # Check if all jobs are completed
            if tracker.is_all_jobs_completed(user_id, parent_job_id, total_chunks):
                log_msg = f'All {total_chunks} chunks completed for parent job {parent_job_id}. SignalR notification sent.'
                
                # Enqueue completion notification
                try:
                    queue_client = QueueClient.from_connection_string(blob_conn_str, "completion-notification-queue")
                    notification_msg = {
                        "user_id": user_id,
                        "parent_job_id": parent_job_id,
                        "log_msg": log_msg
                    }
                    encoded_message = base64.b64encode(json.dumps(notification_msg).encode('utf-8')).decode('utf-8')
                    queue_client.send_message(encoded_message)
                    logging.info(f'Enqueued completion notification for parent job {parent_job_id}')
                except Exception as enqueue_err:
                    logging.error(f'Failed to enqueue completion notification: {str(enqueue_err)}')
                
                # Clean up completed job entities
                tracker.cleanup_completed_jobs(user_id, parent_job_id)



        except Exception as e:
            logging.error(f'Error processing job: {str(e)}')
    
    logging.info("Queue-triggered functions registered")
