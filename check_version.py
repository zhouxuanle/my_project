import azure.functions as func
print(f"Azure Functions version: {func.__version__ if hasattr(func, '__version__') else 'unknown'}")
try:
    print(f"Has signalr_output: {hasattr(func.FunctionApp, 'signalr_output')}")
except Exception as e:
    print(f"Error checking signalr_output: {e}")
