# Universal AI Data Orchestrator - AI Coding Agent Instructions

## Project Vision
Building a **cloud-agnostic, GenAI-powered data orchestration platform** that generates e-commerce test data and processes it through enterprise-grade pipelines. Currently implementing **V1.0: Orchestrated Data Cleaning & Loading** with planned evolution toward multi-cloud support (Azure/AliCloud) and agentic workflows.

## Architecture Overview

### Multi-Tier System
```
Frontend (React + Vite) ←→ Backend (Flask REST API) ←→ Azure Functions ←→ Azure Services
                                        ↓
                          Data Generators (Faker-based)
                                        ↓
                          ADLS Gen2 → ADF Pipelines → Synapse/MySQL
```

### Key Components
- **Backend** (`backend/`): Flask API with JWT auth, MySQL connection pooling, and Azure blob/queue integration
- **Azure Functions** (`backend/myfunc/`): Event-driven processing (SignalR, queue triggers, timers)
- **Frontend** (`frontend/`): React 19 + Vite with Zustand state management and SignalR real-time updates
- **Data Generators** (`backend/data_generators/`): 10+ table generators using Faker with intentional error injection (30% error rate for data quality testing)

### Data Flow: Medallion Architecture
```
Bronze (Raw): shanlee-raw-data/{userId}/{jobId}.json
  ↓ Small (<10k): Pandas transformation (10-min trigger)
  ↓ Large (>10k): Databricks PySpark (daily at 02:00 UTC)
Silver (Cleaned): silver/cleaned/{userId}/{parentJobId}/{jobId}.parquet
Gold (Analytics): gold/analytics/{userId}/{parentJobId}/{jobId}/*.parquet
  ↓
Synapse Analytics + Azure MySQL
```

**Critical Pattern**: Raw data is **read-only source**. Never duplicate to Bronze during cleaning—transformations read from `shanlee-raw-data/` and write to `silver/cleaned/` paths.

## Development Workflows

### Running the Stack
```bash
# Backend (Flask) - Terminal 1
cd backend
python -m venv my_env
my_env\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py  # Runs on http://127.0.0.1:5000

# Frontend (Vite) - Terminal 2
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000

# Azure Functions (local) - Terminal 3
cd backend/myfunc
func host start  # Or use VS Code task: "func: host start"
```

### Environment Setup
- **Backend**: Requires `.env` with `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `JWT_SECRET_KEY`, `AZURE_STORAGE_CONNECTION_STRING`
- **Frontend**: Uses Vite env vars (`VITE_API_URL`)
- **Azure Functions**: Requires `local.settings.json` (⚠️ **NEVER commit** - contains live Azure credentials)

### Testing Data Generation
1. Use frontend UI to trigger generation jobs
2. Data flows: Frontend → Backend `/generate_data` → Azure Queue → Functions → Blob Storage
3. Monitor via SignalR real-time notifications in browser

## Project-Specific Conventions

### Backend Patterns
- **Blueprint Structure**: Routes organized as Flask blueprints (`auth_bp`, `data_bp`, `jobs_bp`, `notifications_bp`)
- **Database**: PyMySQL with DBUtils connection pooling (6 max connections, 2 min cached)
- **Proxy Configuration**: Auto-proxy setup in `utils.py` for China network environments (configurable via `PROXY_HOST`/`PROXY_PORT`)
- **Data Routing** (`data_routing.py`): Automatic queue selection based on record count (≤10k → small-batch-queue, >10k → large-batch-queue)

### Azure Functions Organization
```
backend/myfunc/
├── function_app.py          # Entry point - MUST remain at root (Azure runtime requirement)
├── functions/               # Modular function definitions
│   ├── __init__.py         # Exports register_*_functions
│   ├── signalr_functions.py
│   ├── queue_functions.py
│   ├── small_batch_functions.py
│   └── utils/              # Shared utilities (job tracking, ADF triggers)
```
**Pattern**: Each module exports a `register_*_functions(app)` callable that registers functions to the main `FunctionApp` instance.

### Frontend Patterns
- **API Client** (`services/api.js`): Centralized fetch wrapper with automatic JWT refresh logic
- **State Management**: Zustand stores (minimal, not Redux)
- **Auth Flow**: JWT access tokens (15 min) + refresh tokens (7 days) stored in localStorage
- **Real-time Updates**: SignalR connection for job progress and notifications

### Data Generator Pattern
Each table generator (`backend/data_generators/{table}_table/`) follows:
1. Loads pre-generated realistic data from `data/*.txt` files (usernames, emails, addresses, etc.)
2. Uses `get_random_with_error(data, error_rate=0.3)` to inject deliberate data quality issues
3. Returns dict records via `DataGenerator` class methods in `generate_event_tracking_data.py`

**Why Intentional Errors?** To simulate real-world data quality challenges for downstream cleaning pipelines.

## Critical Integration Points

### SignalR Flow
1. Frontend negotiates connection via `/negotiate` endpoint (Azure Functions)
2. Azure Functions send messages to SignalR hub (`user_{userId}` target)
3. Frontend `SignalRContext` listens and updates UI state

### ADF Pipeline Triggers
- **Small Batch**: Time trigger (every 10 minutes) → polls `small-batch-queue` → calls Azure Function
- **Large Batch**: Time trigger (daily 02:00 UTC) → polls `large-batch-queue` → triggers Databricks notebook
- Completion tracked via `JobProgress` Azure Table Storage entity

### Multi-Destination Loading
ADF pipelines load cleaned data to:
1. **Azure Synapse** (Data Warehouse): Parquet files for analytics
2. **Azure MySQL** (Operational DB): Relational tables for app queries

## Known Issues & Security Notes

### Security Priorities (from IMPROVEMENT_PLAN.md)
- ⚠️ **JWT Secret**: Never use fallback `'super-secret-key'` in production
- ⚠️ **Debug Mode**: `app.run(debug=True)` is hardcoded - make environment-dependent
- ⚠️ **localStorage Tokens**: Current JWT storage vulnerable to XSS (consider httpOnly cookies for production)
- ⚠️ **local.settings.json**: Contains live Azure keys - MUST be in `.gitignore`

### Dead Code Cleaned
The following files were intentionally removed (do NOT recreate):
- `backend/call_data_func.py`, `check_version.py`, `inspect_func.py`
- `frontend/src/App.test.js`, `frontend/src/reportWebVitals.js`

## Roadmap Context

**Current Phase**: V1.0 - Orchestrated Data Cleaning & Loading  
**Next Phases**:
- V2.0: Multi-cloud support (AliCloud OSS, FunctionCompute)
- V3.0: GenAI integration (LangChain schema generation, LangGraph agents)
- V4.0: Enterprise platform (DBT transformations, FinOps dashboard)

See `ROADMAP.md` for detailed feature plans and `IMPROVEMENT_PLAN.md` for prioritized technical debt.

## Common Tasks

### Adding a New Data Table Generator
1. Create `backend/data_generators/{table}_table/{table}_data.py`
2. Add pre-generated data files in `data/` subdirectory
3. Implement `generate_{table}_data()` function with error injection
4. Register method in `DataGenerator` class (`generate_event_tracking_data.py`)
5. Update `append_data()` in `routes/data.py` to handle new table

### Adding a New Azure Function
1. Create module in `backend/myfunc/functions/{name}_functions.py`
2. Define `register_{name}_functions(app: func.FunctionApp)` function
3. Import and call in `function_app.py`
4. Update `functions/__init__.py` to export registration function

### Modifying Transformation Logic
- **Small Batch**: Edit `backend/transformations/pandas/pandas_transforms.py`
- **Large Batch**: Edit PySpark notebooks in Azure Databricks workspace
- Both use shared transformation patterns defined in `transformations/pandas/tables/` modules

## External Dependencies

### Azure Services Required
- **ADLS Gen2**: Raw data storage (`shanlee-raw-data` container)
- **Storage Queue**: Data routing (small-batch-queue, large-batch-queue)
- **SignalR Service**: Real-time frontend updates
- **Data Factory**: Pipeline orchestration and scheduling
- **Table Storage**: Job progress tracking
- **Databricks** (future): Large batch PySpark processing
- **Synapse Analytics**: Data warehouse destination
- **Azure MySQL**: Operational database

### Key Python Packages
- `flask-jwt-extended`: JWT authentication (access + refresh tokens)
- `pymysql` + `dbutils`: MySQL connection pooling
- `faker` + `faker-commerce`: Test data generation
- `pandas`: Small batch transformations
- `azure-storage-blob/queue/file-datalake`: Azure SDK integrations

### Frontend Dependencies
- `@microsoft/signalr`: Real-time connection management
- `zustand`: Lightweight state management (auth store pattern)
- `react-router-dom`: Client-side routing with protected routes

## Tips for AI Agents

1. **Always check ROADMAP.md** before implementing new features - align with phased approach
2. **Respect the Medallion pattern** - never write to Bronze, only read from it
3. **Follow Azure Functions structure rules** - `function_app.py` must stay at root level
4. **Test with intentional errors** - data generators include 30% error rate by design
5. **Consider proxy settings** - China network environment requires `setup_proxy()` call
6. **Check IMPROVEMENT_PLAN.md** for known technical debt before refactoring
