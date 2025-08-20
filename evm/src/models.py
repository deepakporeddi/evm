from typing import Optional, List
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, Index, UniqueConstraint

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    registrations: List["Registration"] = Relationship(back_populates="user")

class Event(SQLModel, table=True):
    __tablename__ = "events"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    location: str = Field(index=True)
    start_time_utc: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    end_time_utc: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    max_capacity: int

    registrations: List["Registration"] = Relationship(back_populates="event")

    __table_args__ = (
        Index("idx_event_name", "name"),
        Index("idx_event_location", "location"),
    )

class Registration(SQLModel, table=True):
    __tablename__ = "registrations"
    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="uq_event_user"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    event: Optional[Event] = Relationship(back_populates="registrations")
    user: Optional[User] = Relationship(back_populates="registrations")
