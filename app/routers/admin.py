from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..dependencies import get_storage, require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def get_stats(storage=Depends(get_storage), _: None = Depends(require_admin)) -> dict:
    return storage.stats()


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, storage=Depends(get_storage), _: None = Depends(require_admin)) -> Response:
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    storage.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
