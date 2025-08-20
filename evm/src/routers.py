from __future__ import annotations
from typing import List, Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from .db import get_session
from . import services
from .lib.exceptions import BadRequestException, NotFoundException, InternalServerException
from .schemas import EventCreate, EventGet, AttendeeCreate, AttendeeGet, PaginatedAttendees, ErrorResponse
from .models import Event
from .time_utils import convert_utc_to_tz

router = APIRouter(prefix="/api", responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})

@router.post("/events", response_model=EventGet, status_code=201)
async def create_event(payload: EventCreate, db: AsyncSession = Depends(get_session)):
    try:
        ev = await services.create_event(
            db,
            name=payload.name,
            location=payload.location,
            start_time=payload.start_time,
            end_time=payload.end_time,
            max_capacity=payload.max_capacity,
        )
    except Exception as e:
        raise BadRequestException(f"{e}")
    return EventGet(
        id=ev.id,
        name=ev.name,
        location=ev.location,
        start_time=convert_utc_to_tz(ev.start_time_utc, "Asia/Kolkata"),
        end_time=convert_utc_to_tz(ev.end_time_utc, "Asia/Kolkata"),
        max_capacity=ev.max_capacity,
    )

@router.get("/events", response_model=List[EventGet])
async def list_events(tz: Literal["Asia/Kolkata", "UTC"] = Query(default="Asia/Kolkata"), db: AsyncSession = Depends(get_session)):
    events = await services.list_upcoming_events(db)
    return [
        EventGet(
            id=e.id,
            name=e.name,
            location=e.location,
            start_time=convert_utc_to_tz(e.start_time_utc, tz),
            end_time=convert_utc_to_tz(e.end_time_utc, tz),
            max_capacity=e.max_capacity,
        )
        for e in events
    ]

@router.post("/events/{event_id}/register", response_model=AttendeeGet, status_code=201, responses={409: {"model": ErrorResponse}})
async def register(event_id: int, payload: AttendeeCreate, db: AsyncSession = Depends(get_session)):
    try:
        user = await services.register_attendee(db, event_id, payload.name, payload.email)
        return AttendeeGet(id=user.id, name=user.name, email=user.email)
    except ValueError as ve:
        msg = str(ve)
        if msg == "EVENT_NOT_FOUND":
            raise NotFoundException("Event not found")
        if msg == "EVENT_FULL":
            raise BadRequestException("Registration closed: event at max capacity")
        if msg == "ALREADY_REGISTERED":
            raise HTTPException(status_code=409, detail="Attendee already registered for this event")
        raise InternalServerException(msg)

@router.get("/events/{event_id}/attendees", response_model=PaginatedAttendees)
async def attendees(event_id: int, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100),
                    db: AsyncSession = Depends(get_session)):
    event = await db.get(Event, event_id)
    if event is None:
        raise NotFoundException("Event not found")
    total, items = await services.list_attendees(db, event_id, page, page_size)
    return PaginatedAttendees(
        total=total,
        page=page,
        page_size=page_size,
        items=[AttendeeGet(**each.model_dump()) for each in items]
    )