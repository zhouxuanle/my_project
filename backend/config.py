import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    # Database Configuration
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    # JWT Configuration
    # Keep reasonably short access token lifetime and longer refresh token lifetime
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 900)))  # default 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 7)))  # default 7 days

    # Azure Configuration
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

    # Data Processing Configuration
    BATCH_SIZE = 100 # Batch size for data generation jobs

    # Proxy Configuration
    PROXY_HOST = os.environ.get('PROXY_HOST', '127.0.0.1')
    PROXY_PORT = int(os.environ.get('PROXY_PORT', 7890))
