from threading import Lock
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, func, select

from database import create_db_and_tables, get_session
from models import (
    Availability,
    Event,
    EventCreate,
    EventStatus,
    EventUpdate,
    Reservation,
    ReservationCreate,
)


app = FastAPI(title="College Events and Reservations API")
reservation_lock = Lock()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_event_or_404(event_id: int, session: Session) -> Event:
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


def count_reservations(event_id: int, session: Session) -> int:
    statement = select(func.count(Reservation.id)).where(
        Reservation.event_id == event_id
    )
    return session.exec(statement).one()


@app.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, session: Session = Depends(get_session)):
    """Create a new workshop, hackathon, seminar, or technical event."""
    db_event = Event.model_validate(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@app.get("/events", response_model=List[Event])
def read_events(session: Session = Depends(get_session)):
    """Return all events."""
    return session.exec(select(Event)).all()


@app.get("/events/{event_id}", response_model=Event)
def read_event(event_id: int, session: Session = Depends(get_session)):
    """Return one event."""
    return get_event_or_404(event_id, session)


@app.put("/events/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event_update: EventUpdate,
    session: Session = Depends(get_session),
):
    """Update event information."""
    db_event = get_event_or_404(event_id, session)
    update_data = event_update.model_dump(exclude_unset=True)

    booked = count_reservations(event_id, session)
    new_capacity = update_data.get("capacity")
    if new_capacity is not None and new_capacity < booked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Capacity cannot be less than the {booked} existing reservations",
        )

    for key, value in update_data.items():
        setattr(db_event, key, value)

    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@app.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    """Delete an event and its associated reservations."""
    db_event = get_event_or_404(event_id, session)
    reservations = session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()
    for reservation in reservations:
        session.delete(reservation)
    session.delete(db_event)
    session.commit()
    return None


@app.post(
    "/events/{event_id}/reserve",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    event_id: int,
    reservation: ReservationCreate,
    session: Session = Depends(get_session),
):
    """Reserve one seat while enforcing event status and capacity."""
    with reservation_lock:
        event = get_event_or_404(event_id, session)
        if event.status != EventStatus.OPEN:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Reservations are closed for this event",
            )

        booked = count_reservations(event_id, session)
        if booked >= event.capacity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event is full; no seats are available",
            )

        db_reservation = Reservation.model_validate(
            reservation, update={"event_id": event_id}
        )
        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)
        return db_reservation


@app.get("/events/{event_id}/reservations", response_model=List[Reservation])
def read_reservations(event_id: int, session: Session = Depends(get_session)):
    """Return all reservations for an event."""
    get_event_or_404(event_id, session)
    return session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()


@app.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int, session: Session = Depends(get_session)
):
    """Cancel a reservation."""
    reservation = session.get(Reservation, reservation_id)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )
    session.delete(reservation)
    session.commit()
    return None


@app.get("/events/{event_id}/availability", response_model=Availability)
def read_availability(event_id: int, session: Session = Depends(get_session)):
    """Return capacity, booked seats, and remaining seats."""
    event = get_event_or_404(event_id, session)
    booked = count_reservations(event_id, session)
    return Availability(
        capacity=event.capacity,
        booked=booked,
        remaining=max(event.capacity - booked, 0),
    )
