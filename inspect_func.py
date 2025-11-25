import azure.functions as func
import inspect

print(f"Version: {func.__version__}")
print("Dir of func:", dir(func))
print("Dir of FunctionApp:", dir(func.FunctionApp))
