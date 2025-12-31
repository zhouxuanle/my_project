Project Overview: I am building a "Universal AI Data Orchestrator." Current Tech Stack: Flask (Backend), React (Frontend), Azure (ADLS Gen2, Data Factory, Databricks). Current Status: Stage 1 (Basic Faker-based e-commerce generation) is functional. The Goal: Evolve the app into a cloud-agnostic platform that uses GenAI to interpret user data requirements and orchestrates pipelines across Azure and Alibaba Cloud. Architecture Goal: Implement an "Adapter Pattern" for multi-cloud support (Azure vs. AliCloud) and an "Agentic Workflow" (LangGraph) for dynamic data generation. Next Immediate Task: Implement Phase 1: Linking the Flask backend to Azure Data Factory (ADF) to trigger a professional Medallion Architecture (Bronze/Silver/Gold) cleaning pipeline. Reference Document: I have a ROADMAP.md file with 4 Phases (V1.0 - V4.0). Please help me implement the current active phase.


# 🚀 Project Roadmap: Universal AI Data Orchestrator

## 📋 V1.0: Orchestrated Data Cleaning & Loading (Stage 2)
**Goal:** Implement a production-ready, dual-path ETL pipeline based on data volume.
- [ ] **Data Routing Logic:**
    - [ ] Update Azure Function to check data size upon "Clean Data" request.
    - [ ] Logic: Send to `small-queue` if <= 10k records; else send to `large-queue`.
- [ ] **Small Batch Pipeline (Fast Path):**
    - [ ] Set up ADF Pipeline with a 10-minute trigger to monitor `small-queue`.
    - [ ] Develop Azure Function using **Pandas** for transformation logic.
- [ ] **Large Batch Pipeline (Heavy Path):**
    - [ ] Set up ADF Pipeline with a Daily trigger to monitor `large-queue`.
    - [ ] Develop **Azure Databricks (PySpark)** notebook for heavy data cleaning.
- [ ] **Multi-Destination Loading:**
    - [ ] Configure ADF to load cleaned data into **Azure Synapse** (Data Warehouse).
    - [ ] Configure ADF to load cleaned data into **Azure MySQL** (Operational DB).
- [ ] **Status & Notification:**
    - [ ] Integrate **SignalR** with ADF to push "Cleaning Complete" notifications to the UI.


## ☁️ V2.0: Multi-Cloud & Hybrid Bridge (AliCloud)
**Goal:** Break the Azure-only lock-in and enable cross-cloud portability.
- [ ] **Adapter Pattern Refactor:** Create a generic `StorageService` interface in the Flask backend.
- [ ] **AliCloud Integration:** Implement `AliCloudOSSAdapter` for storage and `FunctionCompute` for cleaning.
- [ ] **Cloud Selection UI:** Add a frontend toggle allowing users to choose the target cloud provider.
- [ ] **Cross-Cloud Sync:** Build logic to move/sync datasets between Azure and Alibaba Cloud.

## 🧠 V3.0: GenAI & Intelligent Orchestration
**Goal:** Use LLMs to automate schema generation and infrastructure code.
- [ ] **Dynamic AI Generator:** Use LangChain to turn natural language prompts into custom Faker schemas.
- [ ] **Agentic Data Auditor:** Build a **LangGraph** agent to inspect data quality and explain fixes.
- [ ] **Semantic Search (RAG):** Store generated schemas/metadata in ChromaDB for semantic discovery.
- [ ] **Infrastructure Translator:** Use AI to automatically rewrite ETL scripts for AWS or GCP on demand.

## 🏛️ V4.0: Enterprise Platform & FinOps
**Goal:** Focus on cost management, standardization, and professional scaling.
- [ ] **Standardization:** Integrate **DBT (Data Build Tool)** for cloud-agnostic transformation templates.
- [ ] **FinOps Dashboard:** React analytics page showing real-time cloud cost estimates for Azure vs. AliCloud.
- [ ] **Enterprise Security:** Centralize all secrets and keys in **Azure Key Vault**.