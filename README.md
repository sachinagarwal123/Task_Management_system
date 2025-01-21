# Task Management System API

A FastAPI-based REST API for managing tasks with JWT authentication.

## Features

- User authentication with JWT tokens
- CRUD operations for tasks
- PostgreSQL database integration
- Health check endpoint
- Automatic database schema creation
- Input validation using Pydantic

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task-management-system
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv task_env
task_env\Scripts\activate

# Linux/Mac
python3 -m venv task_env
source task_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following content:
```env
DATABASE_URL=postgresql://postgres:your_password_here@localhost/taskdb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Create the database:
```sql
-- In PostgreSQL shell (psql)
CREATE DATABASE taskdb;
```

## Start by initializing migrations:
1. alembic init migrations

## Create the database migration script:
alembic revision --autogenerate -m "Initial migration"

## run the database migration
alembic upgrade head


## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation at: http://localhost:8000/docs

## API Endpoints

### Authentication

#### Register a new user
```http
POST /register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

#### Login
```http
POST /token
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

### Tasks

#### Create a task
```http
POST /tasks/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "My Task",
    "description": "Task description",
    "status": "pending"
}
```

#### Get all tasks
```http
GET /tasks/
Authorization: Bearer <your_token>
```

#### Update a task
```http
PUT /tasks/{task_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "Updated Task",
    "description": "Updated description",
    "status": "in-progress"
}
```

#### Delete a task
```http
DELETE /tasks/{task_id}
Authorization: Bearer <your_token>
```

### Health Check

```http
GET /health
```

## Data Models

### Task
- `id`: UUID (auto-generated)
- `title`: String (required)
- `description`: String (optional)
- `status`: Enum ('pending', 'in-progress', 'completed')
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-updated)
- `user_id`: UUID (auto-assigned)

### User
- `id`: UUID (auto-generated)
- `email`: String (unique, required)
- `password`: String (hashed)
- `created_at`: DateTime (auto-generated)

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Successful operation
- 201: Resource created
- 400: Bad request
- 401: Unauthorized
- 404: Resource not found
- 500: Internal server error

## Security

- Password hashing using bcrypt
- JWT token authentication
- User-specific task access
- Environment variables for sensitive data





