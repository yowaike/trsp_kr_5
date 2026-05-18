# FastAPI Task Manager

Проект реализует REST API для управления задачами, WebSocket-чат с комнатами и базовые зависимости для прав доступа.

## Запуск локально

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Запуск тестов

```bash
pytest
```

## Запуск через Docker

```bash
docker compose up --build
```

## Маршруты

- `GET /health` — проверка состояния
- `POST /tasks` — создание задачи
- `GET /tasks` — список задач текущего пользователя
- `GET /tasks/{task_id}` — получение задачи
- `PATCH /tasks/{task_id}/status` — изменение статуса
- `DELETE /tasks/{task_id}` — удаление задачи
- `GET /users/me` — информация о текущем пользователе
- `GET /users/{user_id}` — информация о пользователе
- `GET /admin/stats` — статистика задач (admin)
- `DELETE /admin/tasks/{task_id}` — удаление задачи (admin)
- `GET /rooms/{room_id}/users` — список пользователей комнаты
- `WebSocket /ws/rooms/{room_id}?username=...` — чат комнаты

## Пример проверки

```bash
curl http://localhost:8000/tasks -H "X-User-Id: 10"
```

Ожидаемый ответ:

```json
[]
```
