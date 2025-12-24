# Azure Functions Structure

This directory contains organized Azure Function modules for better maintainability and scalability.

## Directory Structure

```
functions/
├── __init__.py                 # Package initialization
├── signalr_functions.py        # SignalR-related functions
├── queue_functions.py          # Queue-triggered functions
└── README.md                   # This file
```

## How It Works

Each module contains a `register_xxx_functions(app)` function that registers its functions with the main FunctionApp instance. This approach provides:

- **Separation of Concerns**: Each file handles a specific type of function
- **Easy Navigation**: Find functions by their purpose/trigger type
- **Scalability**: Add new modules without cluttering the main file
- **Maintainability**: Changes to one function type don't affect others

## Adding New Functions

### 1. Create a New Module

Create a new file in the `functions/` directory (e.g., `http_functions.py`):

```python
"""
HTTP-triggered Azure Functions
"""
import azure.functions as func
import logging


def register_http_functions(app: func.FunctionApp):
    """Register all HTTP-triggered functions to the main app"""
    
    @app.function_name(name="my_http_function")
    @app.route(route="myroute", auth_level=func.AuthLevel.ANONYMOUS)
    def my_http_function(req: func.HttpRequest):
        """Your function logic here"""
        return func.HttpResponse("Hello!", status_code=200)
    
    logging.info("HTTP functions registered")
```

### 2. Register in Main App

Import and register your module in [function_app.py](../function_app.py):

```python
from functions.http_functions import register_http_functions

# ... existing code ...

register_http_functions(app)
```

## Current Function Modules

### signalr_functions.py
- **negotiate**: SignalR connection negotiation endpoint
- Used for real-time communication with clients

### queue_functions.py
- **process_data_generation_job**: Queue-triggered function for processing data generation jobs
- Handles message processing, data generation, blob storage uploads, and SignalR notifications

## Best Practices

1. **Group by Trigger Type**: Keep functions with similar triggers together (HTTP, Queue, Timer, etc.)
2. **Single Responsibility**: Each module should handle one type of functionality
3. **Documentation**: Add docstrings to explain each function's purpose
4. **Error Handling**: Include proper try-catch blocks and logging
5. **Configuration**: Use environment variables for configuration (never hardcode secrets)

## Testing

After making changes, test locally with:

```bash
func start
```

Verify that all functions are loaded and accessible:
- Check the console output for registered functions
- Test HTTP endpoints with curl/Postman
- Test queue triggers by adding messages to queues
