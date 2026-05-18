from typing import Any, Dict, List, Optional

from fastapi import WebSocket

from .schemas import Task, TaskCreate, TaskStatus


class Storage:
    def __init__(self) -> None:
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def create_task(self, owner_id: int, task_data: TaskCreate) -> Task:
        task = Task(id=self.next_id, owner_id=owner_id, **task_data.model_dump())
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def list_tasks(
        self,
        owner_id: int,
        status: Optional[TaskStatus] = None,
        min_priority: Optional[int] = None,
    ) -> List[Task]:
        tasks = [task for task in self.tasks.values() if task.owner_id == owner_id]
        if status is not None:
            tasks = [task for task in tasks if task.status == status]
        if min_priority is not None:
            tasks = [task for task in tasks if task.priority >= min_priority]
        return tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def delete_task(self, task_id: int) -> None:
        self.tasks.pop(task_id, None)

    def stats(self) -> Dict[str, Any]:
        by_status = {status.value: 0 for status in TaskStatus}
        for task in self.tasks.values():
            by_status[task.status.value] += 1
        return {"total_tasks": len(self.tasks), "by_status": by_status}


class RoomManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    def connect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        self.rooms.setdefault(room_id, {})[username] = websocket

    def disconnect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        room = self.rooms.get(room_id)
        if room is None:
            return
        stored = room.get(username)
        if stored is websocket:
            room.pop(username, None)
        if not room:
            self.rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, payload: Any) -> None:
        room = self.rooms.get(room_id)
        if not room:
            return
        for websocket in list(room.values()):
            try:
                await websocket.send_json(payload)
            except Exception:
                pass

    def get_users(self, room_id: str) -> List[str]:
        return list(self.rooms.get(room_id, {}).keys())
