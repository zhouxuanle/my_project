"""
Notification storage operations using Azure Table Storage
"""
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from datetime import datetime
import logging
import os


class NotificationStorage:
    def __init__(self, connection_string):
        if not connection_string:
            raise ValueError("Azure Storage connection string is required")
        self.table_service_client = TableServiceClient.from_connection_string(connection_string)
        self.table_name = 'Notifications'
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Create notifications table if it doesn't exist"""
        try:
            self.table_service_client.create_table(self.table_name)
        except ResourceExistsError:
            pass
    
    def save_notification(self, user_id: str, message: str, status: str = 'completed', parent_job_id: str = None):
        """
        Save a notification to persistent storage
        
        Args:
            user_id: User identifier
            message: Notification message
            status: Job status (completed, failed, etc.)
            parent_job_id: Optional parent job ID for deduplication
            
        Returns:
            notification_id: The RowKey/ID of the created notification, or None if already exists
        """
        table_client = self.table_service_client.get_table_client(self.table_name)
        
        # Check if notification with same details already exists
        existing = self._check_existing_notification(user_id, message, status, parent_job_id)
        if existing:
            logging.info(f'Notification already exists for user {user_id} with same details')
            return None
        
        notification_id = f"{user_id}_{int(datetime.utcnow().timestamp() * 1000)}"
        entity = {
            'PartitionKey': user_id,
            'RowKey': notification_id,
            'message': message,
            'status': status,
            'timestamp': datetime.utcnow().isoformat()
        }
        if parent_job_id:
            entity['parent_job_id'] = parent_job_id
        logging.info(f"Saving notification for user {user_id} with ID {notification_id}")
        table_client.create_entity(entity)
        return notification_id
    
    def _check_existing_notification(self, user_id: str, message: str, status: str, parent_job_id: str = None):
        """
        Check if a notification with the same details already exists
        
        Args:
            user_id: User identifier
            message: Notification message
            status: Job status
            parent_job_id: Optional parent job ID
            
        Returns:
            True if exists, False otherwise
        """
        table_client = self.table_service_client.get_table_client(self.table_name)
        
        query_filter = f"PartitionKey eq '{user_id}' and message eq '{message}' and status eq '{status}'"
        if parent_job_id:
            query_filter += f" and parent_job_id eq '{parent_job_id}'"
        
        entities = list(table_client.query_entities(query_filter))
        return len(entities) > 0
    
    def get_unread_notifications(self, user_id: str):
        """
        Get all unread notifications for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of unread notification entities
        """
        table_client = self.table_service_client.get_table_client(self.table_name)
        
        query_filter = f"PartitionKey eq '{user_id}'"
        entities = list(table_client.query_entities(query_filter))
        
        notifications = []
        for entity in entities:
            notifications.append({
                'id': entity['RowKey'],
                'message': entity.get('message'),
                'status': entity.get('status'),
                'timestamp': entity.get('timestamp')
            })
        
        # Sort by timestamp descending (newest first)
        notifications.sort(key=lambda x: x['timestamp'], reverse=True)
        return notifications
    
    def delete_notification(self, user_id: str, notification_id: str):
        """
        Delete a notification
        
        Args:
            user_id: User identifier
            notification_id: Notification row key
        """
        table_client = self.table_service_client.get_table_client(self.table_name)
        
        try:
            table_client.delete_entity(partition_key=user_id, row_key=notification_id)
            return True
        except Exception as e:
            print(f"Error deleting notification: {e}")
            return False
