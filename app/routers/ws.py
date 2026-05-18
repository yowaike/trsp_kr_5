from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect

from ..dependencies import get_room_manager
from ..schemas import RoomUsers
from ..storage import RoomManager

router = APIRouter(tags=["rooms"])


@router.get("/rooms/{room_id}/users", response_model=RoomUsers)
def get_room_users(room_id: str, room_manager: RoomManager = Depends(get_room_manager)) -> RoomUsers:
    return RoomUsers(room_id=room_id, users=room_manager.get_users(room_id))


@router.websocket("/ws/rooms/{room_id}")
async def websocket_room(
    room_id: str,
    websocket: WebSocket,
    username: str = Query(...),
    room_manager: RoomManager = Depends(get_room_manager),
) -> None:
    if not username or not username.strip():
        await websocket.close(code=1008)
        return

    await websocket.accept()
    room_manager.connect(room_id, username, websocket)
    await room_manager.broadcast(
        room_id,
        {"type": "connect", "room_id": room_id, "username": username},
    )
    try:
        while True:
            message = await websocket.receive_json()
            if message.get("type") != "message":
                continue
            text = str(message.get("text", ""))
            if len(text) > 300:
                await websocket.send_json({"type": "error", "detail": "Message is too long"})
                continue
            await room_manager.broadcast(
                room_id,
                {
                    "type": "message",
                    "room_id": room_id,
                    "username": username,
                    "text": text,
                },
            )
    except WebSocketDisconnect:
        room_manager.disconnect(room_id, username, websocket)
        await room_manager.broadcast(
            room_id,
            {"type": "disconnect", "room_id": room_id, "username": username},
        )
