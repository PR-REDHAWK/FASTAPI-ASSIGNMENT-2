# FastAPI College Assignment

## Project Description

This repository contains two FastAPI REST API assignments for college use cases:

- **Task 1 - Lost and Found System:** Students can report lost or found campus items, update their status, and filter reports by status or category.
- **Task 2 - College Events and Reservations:** Organizers can manage events, while students can reserve seats, view availability, and cancel reservations. The API prevents reservations for closed or full events.

Each task uses its own SQLite database and creates its database tables automatically when the application starts.

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn
- Pydantic email validation

## Installation Steps

1. Open this repository folder in VS Code.
2. Open the integrated PowerShell terminal.
3. Create a virtual environment:

   ~~~powershell
   python -m venv .venv
   ~~~

4. Install the required packages:

   ~~~powershell
   .\.venv\Scripts\python.exe -m pip install fastapi "uvicorn[standard]" sqlmodel email-validator
   ~~~

## Run the FastAPI Applications

Run one task at a time from the repository root.

### Task 1 - Lost and Found System

~~~powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Task1 --host 127.0.0.1 --port 8000 --reload
~~~

Swagger UI: http://127.0.0.1:8000/docs

### Task 2 - College Events and Reservations

~~~powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Task2 --host 127.0.0.1 --port 8010 --reload
~~~

Swagger UI: http://127.0.0.1:8010/docs

## Available Endpoints

### Task 1 - Lost and Found System

- POST /items - Create a lost or found item report.
- GET /items - Return all item reports.
- GET /items/{item_id} - Return one item report.
- PUT /items/{item_id} - Update an item report or its status.
- DELETE /items/{item_id} - Delete an item report.
- GET /items/status/{status} - Filter items by Lost, Found, or Returned status.
- GET /items/category/{category} - Filter items by category.

### Task 2 - College Events and Reservations

- POST /events - Create an event.
- GET /events - Return all events.
- GET /events/{event_id} - Return one event.
- PUT /events/{event_id} - Update event information.
- DELETE /events/{event_id} - Delete an event and its reservations.
- POST /events/{event_id}/reserve - Reserve a seat for an open event with remaining capacity.
- GET /events/{event_id}/reservations - Return reservations for an event.
- DELETE /reservations/{reservation_id} - Cancel a reservation.
- GET /events/{event_id}/availability - Return total, booked, and remaining seats.
