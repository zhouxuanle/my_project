"""
Azure Functions App - Main Entry Point

This is the main function app that registers all Azure Functions.
Functions are organized in separate modules under the 'functions' directory.

Structure:
- functions/signalr_functions.py: SignalR related functions (negotiate, etc.)
- functions/queue_functions.py: Queue-triggered functions (data generation, etc.)
- Add more function modules as needed...

To add new functions:
1. Create a new module in the 'functions' directory
2. Define a register_xxx_functions(app) function
3. Import and call it in this file
"""
import azure.functions as func
import logging

# Import function registration modules
from functions import register_signalr_functions, register_queue_functions

# Initialize the Azure Functions app
app = func.FunctionApp()

# Register all function modules
register_signalr_functions(app)
register_queue_functions(app)

logging.info("All Azure Functions registered successfully")
