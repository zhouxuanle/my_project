# Azure Functions Project Structure - Industry Standards

## ✅ Current Structure (Follows Best Practices)

```
backend/myfunc/
├── function_app.py          # ✅ Main entry point (MUST be at root)
├── host.json
├── local.settings.json
├── requirements.txt
└── functions/               # ✅ Package for organizing function modules
    ├── __init__.py          # ✅ Exports public API
    ├── signalr_functions.py
    ├── queue_functions.py
    └── README.md
```

## Why This Structure?

### 1. `function_app.py` at Root Level ✅
**Must be outside `functions/` folder**

Azure Functions runtime **requires** `function_app.py` to be at the root of your function app directory. This is where the `FunctionApp()` instance is created and discovered by the Azure runtime.

```python
# ✅ Correct: function_app.py at root
backend/myfunc/function_app.py

# ❌ Wrong: Would not be discovered by Azure
backend/myfunc/functions/function_app.py
```

### 2. `__init__.py` Exports Module Interface ✅
**Should export public functions**

Following Python's [PEP 8](https://peps.python.org/pep-0008/) and package design best practices:

```python
# functions/__init__.py
from .signalr_functions import register_signalr_functions
from .queue_functions import register_queue_functions

__all__ = [
    'register_signalr_functions',
    'register_queue_functions',
]
```

**Benefits:**
- ✅ Cleaner imports: `from functions import register_signalr_functions`
- ✅ Clear public API: `__all__` declares what's intended for public use
- ✅ Easier refactoring: Internal module names can change without breaking imports
- ✅ IDE support: Better autocomplete and type hints

**Before (verbose):**
```python
from functions.signalr_functions import register_signalr_functions
from functions.queue_functions import register_queue_functions
```

**After (clean):**
```python
from functions import register_signalr_functions, register_queue_functions
```

## Industry Standards Comparison

### ✅ Our Structure (Recommended)
```
backend/myfunc/
├── function_app.py              # Main entry - registers all functions
├── functions/                   # Function modules organized by category
│   ├── __init__.py             # Package exports
│   ├── signalr_functions.py    # SignalR functions
│   ├── queue_functions.py      # Queue functions
│   └── timer_functions.py      # Timer functions (example)
├── services/                    # Business logic (optional)
│   ├── __init__.py
│   └── data_service.py
└── utils/                       # Shared utilities (optional)
    ├── __init__.py
    └── helpers.py
```

### 🟡 Alternative: Monolithic (Not Recommended for Scale)
```
backend/myfunc/
└── function_app.py              # All 50+ functions in one file ❌
```
**Problems:** Hard to maintain, merge conflicts, slow navigation

### 🟡 Alternative: Individual Folders (Azure Functions v1 style)
```
backend/myfunc/
├── NegotiateFunction/
│   ├── function.json
│   └── __init__.py
└── ProcessDataFunction/
    ├── function.json
    └── __init__.py
```
**Note:** This was the old v1 model. Python v2 model (what you're using) is more flexible.

## Best Practices We're Following

### ✅ 1. Separation of Concerns
Each module handles one category of functions:
- `signalr_functions.py` → Real-time communication
- `queue_functions.py` → Async job processing
- `timer_functions.py` → Scheduled tasks (future)

### ✅ 2. Registry Pattern
Each module exports a `register_xxx_functions(app)` function:
```python
def register_queue_functions(app: func.FunctionApp):
    @app.queue_trigger(...)
    def my_function(...):
        pass
```

### ✅ 3. Single Entry Point
`function_app.py` is minimal and just orchestrates registration:
```python
app = func.FunctionApp()
register_signalr_functions(app)
register_queue_functions(app)
```

### ✅ 4. Package Exports Control
`__init__.py` defines the public API with `__all__`

### ✅ 5. Documentation
Each module has docstrings explaining its purpose

## Scaling Further (Optional)

As your project grows, you can add:

```
backend/myfunc/
├── function_app.py
├── functions/
│   ├── __init__.py
│   ├── http/                    # Group by trigger AND domain
│   │   ├── __init__.py
│   │   ├── auth_functions.py
│   │   └── api_functions.py
│   ├── queue/
│   │   ├── __init__.py
│   │   └── data_functions.py
│   └── timer/
│       ├── __init__.py
│       └── maintenance_functions.py
├── services/                     # Business logic layer
│   ├── __init__.py
│   ├── data_service.py
│   └── notification_service.py
├── models/                       # Data models
│   ├── __init__.py
│   └── schemas.py
└── config/                       # Configuration
    ├── __init__.py
    └── settings.py
```

## References

- [Azure Functions Python Programming Model v2](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=get-started%2Casgi%2Capplication-level&pivots=python-mode-decorators)
- [Python Package Structure (PEP 8)](https://peps.python.org/pep-0008/#package-and-module-names)
- [The Hitchhiker's Guide to Python - Structuring Your Project](https://docs.python-guide.org/writing/structure/)
