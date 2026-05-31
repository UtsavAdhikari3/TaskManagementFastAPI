from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task_schema import TaskCreate


def create_task(db: Session, task_data: TaskCreate, current_user: User):
    if current_user.role.name not in ["ADMIN", "MANAGER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN and MANAGER can create tasks"
        )

    if task_data.assigned_to:
        assigned_user = db.query(User).filter(User.id == task_data.assigned_to).first()

        if not assigned_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found"
            )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        assigned_to=task_data.assigned_to,
        created_by=current_user.id,
        status="PENDING"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks_for_user(db: Session, current_user: User):
    role_name = current_user.role.name

    if role_name == "ADMIN":
        return db.query(Task).all()

    if role_name == "MANAGER":
        return db.query(Task).filter(
            (Task.created_by == current_user.id) |
            (Task.assigned_to == current_user.id)
        ).all()

    return db.query(Task).filter(Task.assigned_to == current_user.id).all()


def get_task_by_id(db: Session, task_id: int, current_user: User):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    role_name = current_user.role.name

    if role_name == "ADMIN":
        return task

    if role_name == "MANAGER":
        if task.created_by == current_user.id or task.assigned_to == current_user.id:
            return task

    if role_name == "USER":
        if task.assigned_to == current_user.id:
            return task

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to view this task"
    )