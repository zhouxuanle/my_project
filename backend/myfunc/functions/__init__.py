"""
Azure Functions modules
This package contains organized function modules

Each module provides a register function that should be called with the main FunctionApp instance.
"""

from .signalr_functions import register_signalr_functions
from .queue_functions import register_queue_functions
from .small_batch_functions import register_small_batch_functions

__all__ = [
    'register_signalr_functions',
    'register_queue_functions',
    'register_small_batch_functions',
]
