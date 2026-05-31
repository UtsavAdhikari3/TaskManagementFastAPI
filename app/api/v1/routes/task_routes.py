from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskStatusUpdate
from app.services.task_service import (
    create_task,
    get_tasks_for_user,
    get_task_by_id,
    update_task_status,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, task_data, current_user)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks_for_user(db, current_user)


@router.get("/{task_id}", response_model=TaskResponse)
def retrieve_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_task_by_id(db, task_id, current_user)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def change_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_task_status(
        db=db,
        task_id=task_id,
        new_status=status_data.status.value,
        current_user=current_user
    )