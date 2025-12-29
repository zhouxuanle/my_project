"""
Notification API routes
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from notification_storage import NotificationStorage
from config import Config

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/notifications/unread', methods=['GET'])
@jwt_required()
def get_unread_notifications():
    """Get all unread notifications for the current user"""
    user_id = get_jwt_identity()
    try:
        notification_storage = NotificationStorage(Config.AZURE_STORAGE_CONNECTION_STRING)
        notifications = notification_storage.get_unread_notifications(user_id)
        return jsonify({
            'success': True,
            'notifications': notifications,
            'count': len(notifications)
        })
    except Exception as e:
        import traceback
        print(f"ERROR in get_unread_notifications: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@notifications_bp.route('/notifications/<notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a specific notification"""
    user_id = get_jwt_identity()
    try:
        notification_storage = NotificationStorage(Config.AZURE_STORAGE_CONNECTION_STRING)
        success = notification_storage.delete_notification(user_id, notification_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
