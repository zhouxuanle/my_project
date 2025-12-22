import azure.functions as func
import logging
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from azure.storage.blob import BlobServiceClient
from generate_event_tracking_data import DataGenerator

app = func.FunctionApp()

@app.function_name(name="negotiate")
@app.route(route="negotiate", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_input_binding(arg_name="connectionInfo", type="signalRConnectionInfo", hubName="shanleeSignalR", connectionStringSetting="AZURE_SIGNALR_CONNECTION_STRING")
def negotiate(req: func.HttpRequest, connectionInfo: str):
    return func.HttpResponse(connectionInfo, mimetype="application/json")

@app.queue_trigger(arg_name="azqueue", queue_name="data-generation-queue",
                   connection="AzureWebJobsStorage")
@app.generic_output_binding(arg_name="signalR", type="signalR", hubName="shanleeSignalR", 
                            connectionStringSetting="AZURE_SIGNALR_CONNECTION_STRING")
def process_data_generation_job(azqueue: func.QueueMessage, signalR: func.Out[str]):
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
            cart = gd.generate_cart_data(products_sku, order)
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
                "order_item": order_item,
                "cart": cart
            })

        # Upload to Azure Blob Storage
        blob_conn_str = os.environ.get('AzureWebJobsStorage')
        blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
        container_name = 'shanlee-raw-data'      
        # Use user_id/parent_job_id as a virtual folder for data isolation
        if user_id:
            blob_name = f'{user_id}/{parent_job_id}/{job_id}.json'
            prefix = f"{user_id}/{parent_job_id}/"
        else:
            # Fallback for legacy jobs without userId
            blob_name = f'{parent_job_id}/{job_id}.json'
            prefix = f"{parent_job_id}/"
        try:
            blob_service_client.create_container(container_name)
        except Exception:
            pass  
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(json.dumps(generated_data, default=str), overwrite=True)
        # Note: This is a simple check. For high concurrency/scale, consider using Table Storage or Durable Functions.
        blobs = list(blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=prefix))
        completed_count = len(blobs)
        
        if completed_count >= total_chunks:
            log_msg = f'All {total_chunks} chunks completed for parent job {parent_job_id}. SignalR notification sent.'
            signalR.set(json.dumps({
                'target': 'JobStatusUpdate',
                'arguments': [{"jobId": parent_job_id, "status": "completed", "message": log_msg}]
            }))
            logging.info(log_msg)
        else:
            logging.info(f'Chunk {job_id} completed. Progress: {completed_count}/{total_chunks} for parent job {parent_job_id}.')

    except Exception as e:
        logging.error(f'Error processing job: {str(e)}')
