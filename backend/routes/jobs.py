from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import json
import base64
import logging
from datetime import datetime
from azure.storage.queue import QueueClient
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from utils import NoProxy
from config import Config

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/generate_raw', methods=['POST'])
@jwt_required()
def generate_job():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    total_count = data.get('dataCount', 1)
    batch_size = Config.BATCH_SIZE  # Use config value

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
    
    # Save metadata to Azure Table Storage
    metadata_result = save_data_metadata(
        user_id=current_user_id,
        parent_job_id=parent_job_id,
        dataCount=total_count
    )
    
    if not metadata_result['success']:
        logging.warning(f"Failed to save metadata for job {parent_job_id}: {metadata_result['message']}")
    
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
                    if len(extracted_data) >= 10:
                        extracted_data = extracted_data[:10]
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

@jobs_bp.route('/delete_folder/<parent_job_id>', methods=['DELETE'])
@jwt_required()
def delete_folder(parent_job_id):
    """
    Delete a folder (parent job) and all its associated blobs from Azure Storage.
    Handles both new format (user_id/parent_job_id/) and legacy format (parent_job_id/).
    Only the owner of the folder can delete it.
    """
    current_user_id = get_jwt_identity()
    
    try:
        with NoProxy():
            connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_name = 'shanlee-raw-data'
            container_client = blob_service_client.get_container_client(container_name)
            
            prefix = f"{current_user_id}/{parent_job_id}"
            blobs = list(container_client.list_blobs(name_starts_with=prefix))
            
            # Separate JSON files and directories
            json_blobs = [blob for blob in blobs if blob.name.endswith('.json')]
            dir_blobs = [blob for blob in blobs if not blob.name.endswith('.json')]
            
            deleted_count = 0
            
            # Delete JSON files first (don't count them)
            for blob in json_blobs:
                container_client.delete_blob(blob.name)
            
            # Then delete directories (count these)
            for blob in dir_blobs:
                container_client.delete_blob(blob.name)
                deleted_count += 1
  
            
            logging.info(f"User {current_user_id} deleted folder {parent_job_id} ({deleted_count} items)")
            
            # Also delete the corresponding metadata from Azure Table Storage
            try:
                table_service_client = TableServiceClient.from_connection_string(
                    conn_str=connection_string
                )
                table_client = table_service_client.get_table_client(table_name='DataGenerationMetadata')
                
                # Delete the metadata entity
                table_client.delete_entity(
                    partition_key=current_user_id,
                    row_key=parent_job_id
                )
                
                logging.info(f"Metadata deleted for folder {parent_job_id}")
            except Exception as metadata_err:
                # Log the error but don't fail the operation since blobs are already deleted
                logging.warning(f"Failed to delete metadata for folder {parent_job_id}: {str(metadata_err)}")
            
            return jsonify({
                'success': True,
                'message': 'Folder deleted successfully',
                'deletedCount': deleted_count
            })
            
    except Exception as e:
        logging.error(f"Error deleting folder {parent_job_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error deleting folder: {str(e)}'
        }), 500


@jobs_bp.route('/read_data_metadata/<parent_job_id>', methods=['GET'])
@jwt_required()
def read_data_metadata(parent_job_id):
    """
    Read data generation metadata for a specific folder.
    
    Args:
        parent_job_id (str): Parent job ID
    
    Returns:
        JSON: Metadata including dataCount or error
    """
    current_user_id = get_jwt_identity()
    
    try:
        with NoProxy():
            connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
            table_service_client = TableServiceClient.from_connection_string(
                conn_str=connection_string
            )
            _ensure_table_exists(table_service_client, 'DataGenerationMetadata')
            table_client = table_service_client.get_table_client(table_name='DataGenerationMetadata')
            
            # Retrieve entity by partition key and row key
            entity = table_client.get_entity(
                partition_key=current_user_id,
                row_key=parent_job_id
            )
            
            # Remove Azure-managed properties
            metadata = {
                k: v for k, v in entity.items() 
                if k not in ('PartitionKey', 'RowKey', 'Timestamp', 'odata.metadata', 'odata.type')
            }
            
            logging.info(f"Metadata retrieved for {parent_job_id}: {metadata}")
            return jsonify({
                'success': True,
                'data': metadata
            }), 200
    except Exception as e:
        logging.error(f"Error reading metadata for {parent_job_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error reading metadata: {str(e)}'
        }), 404

def _ensure_table_exists(table_service_client, table_name):
    """Create table if it doesn't exist"""
    try:
        table_service_client.create_table(table_name)
    except ResourceExistsError:
        pass

# Metadata Management Functions
def save_data_metadata(user_id, parent_job_id, **metadata):
    """
    Save data generation metadata to Azure Table Storage.
    
    Args:
        user_id (str): User ID - used as partition key
        parent_job_id (str): Parent job ID - used as row key
        **metadata: Variable keyword arguments containing metadata to store
                   (e.g., dataCount=1000, totalChunks=10, status='completed')
    
    Returns:
        dict: Success status and metadata entity or error message
    """
    try:
        with NoProxy():
            connection_string = Config.AZURE_STORAGE_CONNECTION_STRING
            table_service_client = TableServiceClient.from_connection_string(
                conn_str=connection_string
            )
            _ensure_table_exists(table_service_client, 'DataGenerationMetadata')
            table_client = table_service_client.get_table_client(table_name='DataGenerationMetadata')
            
            # Create entity with partition key and row key
            entity = {
                'PartitionKey': user_id,
                'RowKey': parent_job_id,
                'Timestamp': datetime.utcnow(),
                **metadata  # Add all metadata parameters
            }
            
            # Insert or replace entity
            table_client.upsert_entity(entity)
            
            logging.info(f"Metadata saved for {parent_job_id}: {metadata}")
            return {
                'success': True,
                'message': 'Metadata saved successfully',
                'entity': entity
            }
    except Exception as e:
        logging.error(f"Error saving metadata for {parent_job_id}: {str(e)}")
        return {
            'success': False,
            'message': f'Error saving metadata: {str(e)}'
        }


