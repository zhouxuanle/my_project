# Development Guide

Guide for developers working on the E-commerce Data Generation Platform.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)
- [Best Practices](#best-practices)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- Git
- Code editor (VS Code recommended)

### Initial Setup

1. **Clone the repository:**
```bash
git clone https://github.com/zhouxuanle/my_project.git
cd my_project
```

2. **Set up backend:**
```bash
cd backend
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
pip install -r requirements.txt
```

3. **Set up frontend:**
```bash
cd frontend
npm install
```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` in backend directory
   - Update with your local configuration

5. **Set up database:**
   - Create MySQL database
   - Run schema creation scripts (see DEPLOYMENT.md)

## Development Environment Setup

### VS Code Extensions

Recommended extensions:

- Python (Microsoft)
- Pylance
- ESLint
- Prettier - Code formatter
- Tailwind CSS IntelliSense
- Azure Functions
- GitLens

### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/my_env/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

### Environment Variables

**Backend (.env):**
```env
# Development settings
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=my_project_dev

JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7

# Azure (optional for local dev)
AZURE_STORAGE_CONNECTION_STRING=UseDevelopmentStorage=true
AZURE_SIGNALR_CONNECTION_STRING=<your-signalr-connection-string>

# Proxy (optional)
PROXY_HOST=127.0.0.1
PROXY_PORT=7890
```

## Project Structure

```
my_project/
├── backend/
│   ├── routes/              # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   ├── data.py         # Data generation routes
│   │   └── jobs.py         # Async job routes
│   ├── myfunc/             # Azure Functions
│   │   └── function_app.py # Function definitions
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── database.py         # Database connection
│   ├── utils.py            # Utilities
│   ├── generate_event_tracking_data.py  # Data generator
│   └── requirements.txt    # Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── stores/         # Zustand stores
│   │   ├── services/       # API services
│   │   ├── hooks/          # Custom hooks
│   │   ├── utils/          # Utilities
│   │   ├── App.jsx         # Main component
│   │   └── index.jsx       # Entry point
│   ├── public/             # Static assets
│   └── package.json        # Dependencies
└── docs/                   # Documentation
    ├── API.md
    ├── DEPLOYMENT.md
    └── DEVELOPMENT.md
```

## Development Workflow

### Starting Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
source my_env/bin/activate  # or my_env\Scripts\activate on Windows
python app.py
```

Backend runs on `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Frontend runs on `http://localhost:3000`

**Terminal 3 - Azure Functions (optional):**
```bash
cd backend/myfunc
func start
```

Functions run on `http://localhost:7071`

### Making Changes

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**

3. **Test locally:**
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

4. **Commit changes:**
```bash
git add .
git commit -m "Description of changes"
```

5. **Push to remote:**
```bash
git push origin feature/your-feature-name
```

6. **Create Pull Request**

## Code Style Guidelines

### Python (Backend)

Follow PEP 8 style guide:

**Naming Conventions:**
- Classes: `PascalCase`
- Functions/Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

**Example:**
```python
from flask import Blueprint, jsonify
import logging

# Constants
MAX_DATA_COUNT = 10000

# Blueprint definition
data_bp = Blueprint('data', __name__)

# Function definition
def generate_user_data():
    """Generate fake user data."""
    try:
        # Implementation
        pass
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None

# Route definition
@data_bp.route('/get_user', methods=['GET'])
def get_user():
    """Retrieve user data from database."""
    return jsonify({"success": True})
```

**Docstrings:**
```python
def complex_function(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        dict: Description of return value
    
    Raises:
        ValueError: When invalid input provided
    """
    pass
```

### JavaScript/React (Frontend)

Follow Airbnb JavaScript Style Guide:

**Naming Conventions:**
- Components: `PascalCase`
- Functions/Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`

**Example:**
```javascript
import React, { useState, useEffect } from 'react';
import { apiService } from '../services';

// Constants
const MAX_RETRIES = 3;

// Component definition
const DataTable = ({ userId }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Event handler
  const handleRefresh = async () => {
    setLoading(true);
    try {
      const result = await apiService.getData();
      setData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Effect
  useEffect(() => {
    handleRefresh();
  }, [userId]);

  return (
    <div className="data-table">
      {loading ? <Spinner /> : <Table data={data} />}
    </div>
  );
};

export default DataTable;
```

**Function Components:**
- Use functional components with hooks
- Keep components small and focused
- Extract logic into custom hooks when appropriate

**Props:**
```javascript
// With PropTypes
import PropTypes from 'prop-types';

DataTable.propTypes = {
  userId: PropTypes.string.isRequired,
  onUpdate: PropTypes.func
};

DataTable.defaultProps = {
  onUpdate: () => {}
};
```

## Testing

### Backend Testing

Using pytest:

```python
# tests/test_auth.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    """Test user registration."""
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'TestPass123'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_login(client):
    """Test user login."""
    # First register
    client.post('/register', json={
        'username': 'testuser',
        'password': 'TestPass123'
    })
    
    # Then login
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'TestPass123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
```

Run tests:
```bash
cd backend
pytest
pytest -v  # verbose
pytest tests/test_auth.py  # specific file
```

### Frontend Testing

Using React Testing Library:

```javascript
// src/components/__tests__/DataTable.test.js
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DataTable from '../DataTable';

describe('DataTable', () => {
  test('renders data table', () => {
    render(<DataTable userId="123" />);
    expect(screen.getByText(/data table/i)).toBeInTheDocument();
  });

  test('fetches and displays data', async () => {
    render(<DataTable userId="123" />);
    
    await waitFor(() => {
      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });
    
    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument();
    });
  });

  test('handles refresh button click', async () => {
    const user = userEvent.setup();
    render(<DataTable userId="123" />);
    
    const refreshButton = screen.getByRole('button', { name: /refresh/i });
    await user.click(refreshButton);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

Run tests:
```bash
cd frontend
npm test
npm test -- --coverage  # with coverage
```

## Debugging

### Backend Debugging

**Using VS Code Debugger:**

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development"
      },
      "args": ["run", "--no-debugger", "--no-reload"],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

**Print Debugging:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"User data: {user_data}")
logger.info("Processing request")
logger.warning("Invalid input detected")
logger.error(f"Database error: {str(e)}")
```

### Frontend Debugging

**Browser DevTools:**
- Console: `console.log()`, `console.error()`
- Network tab: Monitor API requests
- React DevTools: Inspect component state

**VS Code Debugger:**

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome against localhost",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

## Common Tasks

### Adding a New API Endpoint

1. **Define route in backend/routes/:**

```python
# backend/routes/new_feature.py
from flask import Blueprint, request, jsonify

new_feature_bp = Blueprint('new_feature', __name__)

@new_feature_bp.route('/new_endpoint', methods=['POST'])
def new_endpoint():
    data = request.get_json()
    # Process data
    return jsonify({"success": True})
```

2. **Register blueprint in app.py:**

```python
from routes.new_feature import new_feature_bp
app.register_blueprint(new_feature_bp)
```

3. **Add API call in frontend:**

```javascript
// frontend/src/services/api.js
export const newFeature = async (data) => {
  const response = await fetch(`${API_BASE_URL}/new_endpoint`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response.json();
};
```

### Adding a New React Component

1. **Create component file:**

```javascript
// frontend/src/components/NewComponent.jsx
import React from 'react';

const NewComponent = ({ prop1, prop2 }) => {
  return (
    <div className="new-component">
      <h2>New Component</h2>
      {/* Content */}
    </div>
  );
};

export default NewComponent;
```

2. **Export from index:**

```javascript
// frontend/src/components/index.js
export { default as NewComponent } from './NewComponent';
```

3. **Use in parent component:**

```javascript
import { NewComponent } from './components';

<NewComponent prop1="value1" prop2="value2" />
```

### Database Migrations

When schema changes are needed:

1. **Update schema in MySQL:**
```sql
ALTER TABLE users ADD COLUMN new_column VARCHAR(255);
```

2. **Update data generation code:**
```python
# backend/generate_event_tracking_data.py
def generate_user_data(self):
    user_info_data = {
        # ... existing fields
        "new_column": fake.word()
    }
    return user_info_data
```

3. **Update insert statements:**
```python
cursor.execute(
    "INSERT INTO users (..., new_column) VALUES (..., %s)",
    (..., user['new_column'])
)
```

### Adding Dependencies

**Backend:**
```bash
cd backend
source my_env/bin/activate
pip install new-package
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install new-package
# or for dev dependency
npm install --save-dev new-package
```

## Best Practices

### Backend

1. **Error Handling:**
   - Always use try-except blocks
   - Log errors with context
   - Return meaningful error messages

2. **Database Connections:**
   - Use connection pooling
   - Always close connections in finally blocks
   - Use context managers when possible

3. **Security:**
   - Validate all input
   - Use parameterized queries
   - Never log sensitive data
   - Use environment variables for secrets

4. **Performance:**
   - Use batch inserts for multiple records
   - Implement pagination for large datasets
   - Use async endpoints for long-running tasks

### Frontend

1. **State Management:**
   - Keep state as local as possible
   - Use Zustand for global state
   - Avoid prop drilling

2. **Performance:**
   - Use React.memo for expensive components
   - Implement virtualization for large lists
   - Lazy load components when appropriate

3. **API Calls:**
   - Handle loading states
   - Implement error handling
   - Show user feedback
   - Use retry logic for transient errors

4. **Accessibility:**
   - Use semantic HTML
   - Add ARIA labels
   - Ensure keyboard navigation
   - Test with screen readers

## Git Workflow

### Branch Naming

- Features: `feature/description`
- Bugs: `fix/description`
- Hotfixes: `hotfix/description`
- Releases: `release/version`

### Commit Messages

Follow conventional commits:

```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(auth): add password reset functionality
fix(data): correct date formatting in user generation
docs(api): update endpoint documentation
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Azure Functions Python](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Faker Documentation](https://faker.readthedocs.io/)

---

For more information, see [README.md](../README.md) and [API.md](./API.md).
