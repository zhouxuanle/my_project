from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import json
import base64
import logging
from azure.storage.queue import QueueClient
from azure.storage.blob import BlobServiceClient
from utils import NoProxy
from config import Config

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/generate_raw', methods=['POST'])
@jwt_required()
def generate_job():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    total_count = data.get('dataCount', 1)
    batch_size = 1000  # You can adjust this value as needed

    parent_job_id = str(uuid.uuid4())
    job_ids = []
    
    # Calculate total chunks
    total_chunks = (total_count + batch_size - 1) // batch_size

    # Enqueue job to Azure Queue
    # Use NoProxy context to bypass SOCKS5 proxy for Azure SDK
    with NoProxy():
        connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
        queue_name = 'data-generation-queue'
        queue_client = QueueClient.from_connection_string(connection_string, queue_name)
        
        print('queue client created---------------------')
        for start in range(0, total_count, batch_size):
            count = min(batch_size, total_count - start)
            job_id = str(uuid.uuid4())
            message = {
                'userId': current_user_id,
                'parentJobId': parent_job_id, 
                'jobId': job_id, 
                'count': count,
                'totalChunks': total_chunks
            }
            encoded_message = base64.b64encode(json.dumps(message).encode('utf-8')).decode('utf-8')
            queue_client.send_message(encoded_message)
            print(f'message for chunk {job_id} has sent---------------------')
            job_ids.append(job_id)

    print('all chunk messages have been sent---------------------')
    return jsonify({
        'parentJobId': parent_job_id,
        'jobIds': job_ids,
        'status': 'queued',
        'total_count': total_count,
        'batch_size': batch_size,
        'total_chunks': total_chunks
    }), 202

@jobs_bp.route('/get_raw_data/<parent_job_id>/<table_name>', methods=['GET'])
@jwt_required()
def get_raw_data(parent_job_id, table_name):
    current_user_id = get_jwt_identity()
    try:
        with NoProxy():
            connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_name = 'shanlee-raw-data'
            container_client = blob_service_client.get_container_client(container_name)
            
            extracted_data = []
            # Check for chunks (virtual directory) using parent_job_id
            blobs = list(container_client.list_blobs(name_starts_with=f"{current_user_id}/{parent_job_id}/"))
            
            if blobs:
                for blob in blobs:
                    blob_client = container_client.get_blob_client(blob.name)
                    chunk_data = json.loads(blob_client.download_blob().readall())
                    
                    # Extract specific table data from this chunk
                    chunk_extracted = [item.get(table_name) for item in chunk_data if item.get(table_name)]
                    extracted_data.extend(chunk_extracted)
                    
                    # Stop if we have enough data
                    if len(extracted_data) >= 100:
                        extracted_data = extracted_data[:100]
                        break
            else:
                return jsonify({'success': False, 'message': 'Data not found or not ready yet'}), 404
            
            return jsonify({
                'success': True,
                table_name: extracted_data
            })
    except Exception as e:
        logging.error(f"Error retrieving raw data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving data: {str(e)}'
        }), 500

@jobs_bp.route('/list_parent_jobs', methods=['GET'])
@jwt_required()
def list_parent_jobs():
    current_user_id = get_jwt_identity()
    try:
        with NoProxy():
            connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_name = 'shanlee-raw-data'
            container_client = blob_service_client.get_container_client(container_name)
            prefix = f"{current_user_id}/"
            blobs = container_client.list_blobs(name_starts_with=prefix)
            parent_job_ids = set()
            for blob in blobs:
                # blob.name: <user_id>/<parent_job_id>/<...>
                parts = blob.name.split('/')
                if len(parts) > 1:
                    parent_job_ids.add(parts[1])
            return jsonify({
                'success': True,
                'parentJobIds': sorted(parent_job_ids)
            })
    except Exception as e:
        logging.error(f"Error listing parent jobs: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error listing parent jobs: {str(e)}'
        }), 500
