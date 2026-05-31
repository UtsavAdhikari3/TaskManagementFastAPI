# Database ERD

```mermaid
erDiagram
    ROLES ||--o{ USERS : has
    USERS ||--o{ TASKS : assigned_tasks
    USERS ||--o{ TASKS : created_tasks

    ROLES {
        int id PK
        string name
    }

    USERS {
        int id PK
        string email
        string full_name
        string hashed_password
        int role_id FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    TASKS {
        int id PK
        string title
        text description
        string status
        datetime due_date
        int assigned_to FK
        int created_by FK
        datetime created_at
        datetime updated_at
    }
```

## Relationships

- `users.role_id` references `roles.id`
- `tasks.assigned_to` references `users.id`
- `tasks.created_by` references `users.id`

## Notes

- Each user has one role.
- Each role can belong to many users.
- A task can be assigned to one user.
- A task is created by one user.
- `assigned_to` may be nullable if a task is created before assignment.
- `created_by` is required because every task must have a creator.
