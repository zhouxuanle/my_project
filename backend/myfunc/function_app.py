import azure.functions as func
import logging
import os
import json
from azure.storage.blob import BlobServiceClient
from generate_event_tracking_data import DataGenerator
from signalrcore.hub.connection_builder import HubConnectionBuilder

app = func.FunctionApp()

@app.queue_trigger(arg_name="azqueue", queue_name="data-generation-queue",
                   connection="AzureWebJobsStorage")
def process_data_generation_job(azqueue: func.QueueMessage):
    logging.info('Queue trigger received message: %s', azqueue.get_body().decode('utf-8'))
    try:
        # Parse job message
        message = json.loads(azqueue.get_body().decode('utf-8'))
        job_id = message.get('jobId')
        count = int(message.get('count', 1))

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
        blob_conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') or os.environ.get('AzureWebJobsStorage')
        blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
        container_name = 'raw_generated-data'
        blob_name = f'{job_id}.json'
        # Ensure container exists
        try:
            blob_service_client.create_container(container_name)
        except Exception:
            pass  # Container may already exist
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(json.dumps(generated_data, default=str), overwrite=True)
        logging.info(f'Data for job {job_id} uploaded to blob {blob_name} in container {container_name}')

        # Send job status notification via SignalR
        signalr_conn_str = os.environ.get("AZURE_SIGNALR_CONNECTION_STRING")
        # Parse endpoint from connection string
        # Example connection string: Endpoint=https://<your-signalr-name>.service.signalr.net;AccessKey=...;Version=1.0;
        endpoint = None
        for part in signalr_conn_str.split(';'):
            if part.startswith('Endpoint='):
                endpoint = part.replace('Endpoint=', '').strip()
        if endpoint:
            hub_url = f"{endpoint}/DataGenerationHub"  # Replace 'clientHub' with your actual hub name if different
            hub_connection = HubConnectionBuilder()\
                .with_url(hub_url)\
                .build()
            hub_connection.start()
            # Send job status update
            hub_connection.send("JobStatusUpdate", [{"jobId": job_id, "status": "completed"}])
            hub_connection.stop()
            logging.info(f'SignalR notification sent for job {job_id}')
        else:
            logging.error('SignalR endpoint not found in connection string')
    except Exception as e:
        logging.error(f'Error processing job: {str(e)}')
