import os

from fastapi import FastAPI

from .routers import admin, tasks, users, ws

app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(ws.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": os.getenv("APP_ENV", "local")}
