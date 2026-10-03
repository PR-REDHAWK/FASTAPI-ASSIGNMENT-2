# Task 2 - College Events and Reservations API

FastAPI REST API for managing college events and student reservations.

## Run

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Task2 --reload
```

The interactive API documentation is available at `http://127.0.0.1:8000/docs`.

The SQLite database is created automatically as `Task2/database.db` when the application starts.

## API behavior

- Event capacity must be greater than zero.
- Event status is `Open` or `Closed`.
- Reservations require a valid email and an existing, open event.
- Reservations are rejected with HTTP 409 when an event is full or closed.
- Deleting an event also removes its reservations.
- Availability reports `capacity`, `booked`, and `remaining` seats.
