Project Overview: I am building a "Universal AI Data Orchestrator." Current Tech Stack: Flask (Backend), React (Frontend), Azure (ADLS Gen2, Data Factory, Databricks). Current Status: Stage 1 (Basic Faker-based e-commerce generation) is functional. The Goal: Evolve the app into a cloud-agnostic platform that uses GenAI to interpret user data requirements and orchestrates pipelines across Azure and Alibaba Cloud. Architecture Goal: Implement an "Adapter Pattern" for multi-cloud support (Azure vs. AliCloud) and an "Agentic Workflow" (LangGraph) for dynamic data generation. Next Immediate Task: Implement Phase 1: Linking the Flask backend to Azure Data Factory (ADF) to trigger a professional Medallion Architecture (Bronze/Silver/Gold) cleaning pipeline. Reference Document: I have a ROADMAP.md file with 4 Phases (V1.0 - V4.0). Please help me implement the current active phase.


# 🚀 Project Roadmap: Universal AI Data Orchestrator

## 📋 V1.0: Professional Data Pipeline (The Baseline)
- [ ] Implement Medallion Architecture in Azure (Folders: `bronze/`, `silver/`, `gold/`)
- [ ] Connect Flask to Azure Data Factory (ADF) API to trigger pipelines
- [ ] Create "Small Path" Azure Function (Pandas) for quick cleaning
- [ ] Create "Large Path" Databricks Job (PySpark) for big data batches
- [ ] Automated Gold Layer loading into Azure MySQL/Synapse

## ☁️ V2.0: Multi-Cloud & Hybrid Bridge
- [ ] Refactor Backend to use a generic `StorageService` Interface
- [ ] Implement `AliCloudOSSAdapter` (Adapter Pattern)
- [ ] Add Frontend Toggle: [Target Cloud: Azure | AliCloud]
- [ ] Implement Cross-Cloud Data Synchronization logic

## 🧠 V3.0: GenAI & Intelligent Orchestration
- [ ] **AI Generator:** Use LLM to turn user prompts into Faker JSON schemas
- [ ] **Agentic Auditor:** Implement LangGraph to analyze data quality
- [ ] **Vector RAG:** Store generated schemas in ChromaDB for semantic search
- [ ] **Dynamic Infrastructure:** AI-generated scripts for AWS/GCP migration

## 🏛️ V4.0: Enterprise Platform & FinOps
- [ ] **Standardization:** Integrate DBT (Data Build Tool) for cleaning templates
- [ ] **FinOps:** React dashboard for real-time cloud cost estimation
- [ ] **Security:** Centralize all cloud keys in Azure Key Vault