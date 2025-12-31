# Documentation Index

Welcome to the E-commerce Data Generation Platform documentation!

## Quick Start

New to the project? Start here:

1. Read the [Main README](../README.md) for project overview
2. Follow the [Development Guide](./DEVELOPMENT.md) to set up your environment
3. Review the [API Documentation](./API.md) to understand available endpoints
4. When ready to deploy, see the [Deployment Guide](./DEPLOYMENT.md)

## Documentation Structure

### 📘 [Main README](../README.md)
**Start here for an overview of the entire project**

- Project description and key capabilities
- Architecture overview with diagrams
- Complete feature list
- Tech stack details
- Quick installation guide
- Basic configuration
- Usage examples
- Project structure
- Security considerations
- Troubleshooting tips

**Best for:** Understanding what the project does and how to get started

---

### 🔌 [API Documentation](./API.md)
**Complete reference for all API endpoints**

- Authentication endpoints (register, login, refresh)
- Data generation endpoints (synchronous and asynchronous)
- Data retrieval endpoints
- Job management endpoints
- Request/response examples
- Data models and schemas
- Error codes and handling
- Rate limiting information
- Real-time notifications with SignalR
- Code examples in Python and JavaScript

**Best for:** Integrating with the API, understanding endpoints, debugging API issues

---

### 🚀 [Deployment Guide](./DEPLOYMENT.md)
**Production deployment instructions**

- Azure services setup (MySQL, Storage, SignalR, Functions)
- Database schema creation
- Backend deployment options
  - Azure App Service
  - Container deployment
- Frontend deployment options
  - Azure Static Web Apps
  - Azure Blob Storage static website
- Azure Functions deployment
- Environment configuration
- Post-deployment checklist
- Monitoring with Application Insights
- Troubleshooting production issues
- Security best practices
- Cost optimization

**Best for:** Deploying to production, Azure configuration, production troubleshooting

---

### 💻 [Development Guide](./DEVELOPMENT.md)
**Developer workflow and best practices**

- Development environment setup
- VS Code configuration
- Project structure deep dive
- Development workflow
- Git branching strategy
- Code style guidelines
  - Python (PEP 8)
  - JavaScript (Airbnb style)
- Debugging techniques
- Common development tasks
  - Adding API endpoints
  - Creating React components
  - Database migrations
  - Managing dependencies
- Best practices

**Best for:** Day-to-day development, contributing code, maintaining code quality

---

### 🎨 [Frontend README](../frontend/README.md)
**Frontend-specific documentation**

- Frontend tech stack (React, Vite, Tailwind CSS)
- Available npm scripts
- Frontend project structure
- Key features
- Development setup
- Environment variables
- Building for production

**Best for:** Working on the React frontend, understanding frontend architecture

---

### 📂 V1.0 Medallion Docs
Use these together for the V1.0 dual-path pipeline (small: 10-min, large: 10-hour queue-aware).
- [V1.0_SUMMARY.md](./V1.0_SUMMARY.md) – one-page overview and status
- [V1.0_IMPLEMENTATION.md](./V1.0_IMPLEMENTATION.md) – detailed pipelines (Azure Functions + Databricks)
- [V1.0_API.md](./V1.0_API.md) – endpoint reference and flow diagrams
- [V1.0_QUICK_START.md](./V1.0_QUICK_START.md) – hands-on steps and commands

## Documentation by Role

### For New Developers
1. [Main README](../README.md) - Understand the project
2. [Development Guide](./DEVELOPMENT.md) - Set up your environment
3. [Frontend README](../frontend/README.md) - Start with frontend development

### For Backend Developers
1. [API Documentation](./API.md) - Understand endpoints
2. [Development Guide](./DEVELOPMENT.md) - Coding standards and practices
3. [Main README](../README.md) - Architecture overview

### For DevOps/Operations
1. [Deployment Guide](./DEPLOYMENT.md) - Deploy and configure services
2. [Main README](../README.md) - Understand system requirements
3. [API Documentation](./API.md) - Understand service interactions

### For API Consumers
1. [API Documentation](./API.md) - Complete API reference
2. [Main README](../README.md) - Authentication and usage examples

### For Project Managers
1. [Main README](../README.md) - Features and capabilities
2. [API Documentation](./API.md) - Integration possibilities
3. [Deployment Guide](./DEPLOYMENT.md) - Infrastructure requirements

---

## Quick Reference

### Installation
```bash
# Backend
cd backend
python -m venv my_env
source my_env/bin/activate  # Windows: my_env\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Running Locally
```bash
# Backend (Terminal 1)
cd backend
python app.py

# Frontend (Terminal 2)
cd frontend
npm run dev
```

### Common Commands
```bash
# Build frontend
cd frontend && npm run build

# Deploy functions
cd backend/myfunc && func azure functionapp publish <app-name>
```

### Important URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Azure Functions: http://localhost:7071

### Key Environment Variables
```env
# Backend
DB_HOST=your-mysql-host
DB_USER=your-username
DB_PASSWORD=your-password
JWT_SECRET_KEY=your-secret-key
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
```

---

## Contributing to Documentation

When updating documentation:

1. **README.md** - High-level changes, new features, architecture updates
2. **API.md** - New endpoints, changed request/response formats
3. **DEPLOYMENT.md** - Deployment process changes, new services
4. **DEVELOPMENT.md** - New tools, workflow changes, best practices

Keep documentation:
- **Current**: Update with code changes
- **Clear**: Use simple language and examples
- **Complete**: Cover all aspects of the topic
- **Consistent**: Follow existing structure and style

---

## Getting Help

- **Issues**: Check existing issues on GitHub
- **Questions**: Review documentation thoroughly first
- **Bugs**: Include error logs and reproduction steps
- **Features**: Describe use case and expected behavior

---

## License

This project is private and proprietary. All rights reserved.

---

Last Updated: December 2024
