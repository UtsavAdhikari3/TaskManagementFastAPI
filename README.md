# Task Management RBAC API

A backend API system built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT authentication** for managing users, tasks, and role-based access control.

This project was developed as a backend technical task to demonstrate API design, authentication, authorization, relational database modeling, and modular backend architecture.

---

## Features

- User registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Protected routes
- Role-based access control
- Roles:

  - `ADMIN`
  - `MANAGER`
  - `USER`

- Task management APIs
- Task status workflow validation
- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- Docker and Docker Compose setup
- Seed script for default roles and test users
- Swagger/OpenAPI documentation

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT
- Passlib / bcrypt
- Docker
- Docker Compose
- Pydantic

---

## Project Structure

```txt
app/
├── api/
│   └── v1/
│       ├── api.py
│       └── routes/
│           ├── auth_routes.py
│           ├── user_routes.py
│           └── task_routes.py
│
├── core/
│   ├── config.py
│   ├── dependencies.py
│   ├── permissions.py
│   └── security.py
│
├── db/
│   ├── base.py
│   ├── seed.py
│   └── session.py
│
├── models/
│   ├── role.py
│   ├── user.py
│   └── task.py
│
├── schemas/
│   ├── auth_schema.py
│   ├── user_schema.py
│   └── task_schema.py
│
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   └── task_service.py
│
└── main.py
```

---

## Role Permissions

| Feature             | ADMIN |                MANAGER |                USER |
| ------------------- | ----: | ---------------------: | ------------------: |
| View all users      |   Yes |                     No |                  No |
| View all tasks      |   Yes |                     No |                  No |
| Create tasks        |   Yes |                    Yes |                  No |
| Assign tasks        |   Yes |                    Yes |                  No |
| View created tasks  |   Yes |                    Yes |                  No |
| View assigned tasks |   Yes |                    Yes |                 Yes |
| Update task details |   Yes |     Created tasks only |                  No |
| Update task status  |   Yes | Created/assigned tasks | Assigned tasks only |
| Delete tasks        |   Yes |                     No |                  No |

---

## Task Status Workflow

Supported statuses:

```txt
PENDING
IN_PROGRESS
COMPLETED
```

Validation rules:

- Invalid statuses are rejected.
- Completed tasks cannot be moved back to another status.
- New tasks are created with `PENDING` status by default.

---

## Database Schema

### roles

| Column | Type    | Description                     |
| ------ | ------- | ------------------------------- |
| id     | Integer | Primary key                     |
| name   | String  | Role name: ADMIN, MANAGER, USER |

### users

| Column          | Type     | Description             |
| --------------- | -------- | ----------------------- |
| id              | Integer  | Primary key             |
| email           | String   | Unique user email       |
| full_name       | String   | User full name          |
| hashed_password | String   | Hashed password         |
| role_id         | Integer  | Foreign key to roles.id |
| is_active       | Boolean  | Account status          |
| created_at      | DateTime | Created timestamp       |
| updated_at      | DateTime | Updated timestamp       |

### tasks

| Column      | Type     | Description                     |
| ----------- | -------- | ------------------------------- |
| id          | Integer  | Primary key                     |
| title       | String   | Task title                      |
| description | Text     | Task description                |
| status      | String   | PENDING, IN_PROGRESS, COMPLETED |
| due_date    | DateTime | Optional due date               |
| assigned_to | Integer  | Foreign key to users.id         |
| created_by  | Integer  | Foreign key to users.id         |
| created_at  | DateTime | Created timestamp               |
| updated_at  | DateTime | Updated timestamp               |

---

## Relationships

```txt
users.role_id       → roles.id
tasks.assigned_to   → users.id
tasks.created_by    → users.id
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/task_rbac_db
SECRET_KEY=change-this-secret-key-for-development
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

An example file is provided as `.env.example`.

---

## Running the Project with Docker

Build and start the containers:

```bash
docker compose up --build
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

Swagger documentation:

```txt
http://127.0.0.1:8000/docs
```

Health check:

```txt
http://127.0.0.1:8000/health
```

Database health check:

```txt
http://127.0.0.1:8000/db-health
```

---

## Running Migrations

Generate a migration:

```bash
docker compose exec api alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
docker compose exec api alembic upgrade head
```

---

## Seeding Roles and Test Users

Run the seed script:

```bash
docker compose exec api python -m app.db.seed
```

This creates the default roles:

```txt
ADMIN
MANAGER
USER
```

It also creates test users:

| Email                                         | Password    | Role    |
| --------------------------------------------- | ----------- | ------- |
| [admin@gmail.com](mailto:admin@gmail.com)     | Password123 | ADMIN   |
| [manager@gmail.com](mailto:manager@gmail.com) | Password123 | MANAGER |
| [normal@gmail.com](mailto:normal@gmail.com)   | Password123 | USER    |

These users are intended for local development and API testing only.

---

## API Endpoints

### Authentication

| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| POST   | `/api/v1/auth/register` | Register a new user            |
| POST   | `/api/v1/auth/login`    | Login and receive JWT token    |
| GET    | `/api/v1/auth/me`       | Get current authenticated user |

### Users

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/v1/users/` | View all users, ADMIN only |

### Tasks

| Method | Endpoint                         | Description                          |
| ------ | -------------------------------- | ------------------------------------ |
| POST   | `/api/v1/tasks/`                 | Create a task, ADMIN/MANAGER         |
| GET    | `/api/v1/tasks/`                 | Retrieve tasks based on role         |
| GET    | `/api/v1/tasks/{task_id}`        | Retrieve a single task based on role |
| PATCH  | `/api/v1/tasks/{task_id}`        | Update task details                  |
| PATCH  | `/api/v1/tasks/{task_id}/assign` | Assign task to user                  |
| PATCH  | `/api/v1/tasks/{task_id}/status` | Update task status                   |
| DELETE | `/api/v1/tasks/{task_id}`        | Delete task, ADMIN only              |

---

## Example Requests

### Register User

```json
{
  "email": "user@example.com",
  "full_name": "Test User",
  "password": "Password123"
}
```

Newly registered users receive the default `USER` role.

### Login

```json
{
  "email": "admin@gmail.com",
  "password": "Password123"
}
```

Example response:

```json
{
  "access_token": "jwt-token-value",
  "token_type": "bearer"
}
```

Use the returned token in Swagger Authorize or in the request header:

```txt
Authorization: Bearer <token>
```

### Create Task

```json
{
  "title": "Prepare API documentation",
  "description": "Write README and endpoint usage guide",
  "due_date": "2026-06-10T12:00:00Z",
  "assigned_to": 3
}
```

### Update Task Status

```json
{
  "status": "IN_PROGRESS"
}
```

---

## Validation and Error Handling

The API includes validation for:

- Duplicate user emails
- Invalid login credentials
- Missing or invalid JWT tokens
- Role-based unauthorized actions
- Invalid task status values
- Invalid task assignment user IDs
- Completed tasks moving backward in workflow
- Accessing tasks outside user permissions

The API uses proper HTTP status codes such as:

```txt
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Validation Error
```

---

## Testing Checklist

### Authentication

- Register user
- Login user
- Access `/auth/me` with valid token
- Access protected route without token
- Test duplicate registration

### ADMIN

- View all users
- View all tasks
- Create task
- Assign task
- Update task details
- Update task status
- Delete task

### MANAGER

- Cannot view all users
- Can create tasks
- Can assign tasks
- Can view tasks created by or assigned to them
- Can update task status
- Cannot delete tasks

### USER

- Cannot view all users
- Cannot create tasks
- Can view only assigned tasks
- Can update assigned task status
- Cannot assign tasks
- Cannot delete tasks

### Status Workflow

- `PENDING` to `IN_PROGRESS`
- `IN_PROGRESS` to `COMPLETED`
- `COMPLETED` to `PENDING` should fail
- Invalid status should fail

---

## Assumptions and Limitations

- Newly registered users are assigned the `USER` role by default.
- Admin and manager test accounts are created using the seed script.
- Redis was not included because the core task did not require caching or token blacklisting.
- The project focuses on backend API functionality and does not include a frontend.
- JWT logout/token blacklist is not implemented in the current version.
- The current implementation uses synchronous SQLAlchemy.

---

## Future Improvements

- Add unit and integration tests
- Add pagination and filtering for task listing
- Add Redis-based login rate limiting
- Add JWT token blacklist/logout support
- Add refresh tokens
- Add audit logs for task assignment and status changes
- Add CI pipeline for automated testing

---

## Author

Backend technical task implementation using FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, and RBAC.
