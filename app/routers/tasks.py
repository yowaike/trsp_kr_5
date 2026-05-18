from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from ..dependencies import get_current_user, get_storage
from ..schemas import Task, TaskCreate, TaskStatus, TaskStatusUpdate, User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user: User = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Task:
    return storage.create_task(user.id, task_data)


@router.get("", response_model=list[Task])
def list_tasks(
    status: TaskStatus | None = Query(None),
    min_priority: int | None = Query(None, ge=1, le=5),
    user: User = Depends(get_current_user),
    storage=Depends(get_storage),
):
    return storage.list_tasks(user.id, status=status, min_priority=min_priority)


@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    user: User = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Task:
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    user: User = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Task:
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task.status = status_data.status
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    storage=Depends(get_storage),
) -> Response:
    task = storage.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    storage.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
