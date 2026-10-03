from enum import Enum
from typing import Optional

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel


class EventStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"


def require_text(value: str | None) -> str | None:
    """Reject empty or whitespace-only text while preserving optional values."""
    if value is None:
        return None
    value = value.strip()
    if not value:
        raise ValueError("This field must not be empty")
    return value


class EventBase(SQLModel):
    title: str = Field(min_length=1, description="Event name")
    venue: str = Field(min_length=1, description="Event location")
    capacity: int = Field(gt=0, description="Maximum number of participants")
    organizer: str = Field(min_length=1, description="Organizer name")
    status: EventStatus = Field(default=EventStatus.OPEN)

    _clean_title = field_validator("title", mode="before")(require_text)
    _clean_venue = field_validator("venue", mode="before")(require_text)
    _clean_organizer = field_validator("organizer", mode="before")(require_text)


class Event(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1)
    venue: Optional[str] = Field(default=None, min_length=1)
    capacity: Optional[int] = Field(default=None, gt=0)
    organizer: Optional[str] = Field(default=None, min_length=1)
    status: Optional[EventStatus] = None

    _clean_title = field_validator("title", mode="before")(require_text)
    _clean_venue = field_validator("venue", mode="before")(require_text)
    _clean_organizer = field_validator("organizer", mode="before")(require_text)


class ReservationBase(SQLModel):
    student_name: str = Field(min_length=1, description="Participant name")
    roll_number: str = Field(min_length=1, description="Participant roll number")
    email: EmailStr

    _clean_student_name = field_validator("student_name", mode="before")(require_text)
    _clean_roll_number = field_validator("roll_number", mode="before")(require_text)


class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id", index=True)


class ReservationCreate(ReservationBase):
    pass


class Availability(SQLModel):
    capacity: int
    booked: int
    remaining: int
