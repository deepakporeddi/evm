from __future__ import annotations
from typing import Tuple, List

from pydantic import EmailStr
from sqlmodel import select, and_
from sqlalchemy import func, Select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Event, User, Registration
from .time_utils import to_utc_from_ist

async def create_event(db: AsyncSession, *, name: str, location: str, start_time, end_time, max_capacity: int) -> Event:
    ev = Event(
        name=name,
        location=location,
        start_time_utc=to_utc_from_ist(start_time),
        end_time_utc=to_utc_from_ist(end_time),
        max_capacity=max_capacity,
    )
    db.add(ev)
    await db.commit()
    await db.refresh(ev)
    return ev

async def list_upcoming_events(db: AsyncSession) -> list[Event]:
    statement: Select = select(Event).where(Event.end_time_utc >= func.now()).order_by(Event.start_time_utc.asc())
    res = await db.exec(statement)
    events = list(res.all())
    return events

async def get_event(db: AsyncSession, event_id: int) -> Event | None:
    return await db.get(Event, event_id)

async def get_or_create_user(db: AsyncSession, name: str, email: EmailStr) -> User:
    statement: Select = select(User).where(User.email == email)
    res = await db.exec(statement)
    existing = res.first()
    if existing:
        if existing.name != name:
            existing.name = name
            db.add(existing)
            await db.commit()
            await db.refresh(existing)
        return existing
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def count_registrations(db: AsyncSession, event_id: int) -> int:
    statement: Select = select(func.count(Registration.id)).where(Registration.event_id == event_id)
    res = await db.exec(statement)
    val = res.one()
    return int(val)

async def is_registered(db: AsyncSession, event_id: int, user_id: int) -> bool:
    statement: Select = select(Registration).where(Registration.event_id == event_id, Registration.user_id == user_id)
    res = await db.exec(statement)
    return res.first() is not None

async def register_attendee(db: AsyncSession, event_id: int, name: str, email: EmailStr) -> User:
    ev = await get_event(db, event_id)
    if not ev:
        raise ValueError("EVENT_NOT_FOUND")
    if await count_registrations(db, event_id) >= ev.max_capacity:
        raise ValueError("EVENT_FULL")
    user = await get_or_create_user(db, name, email)
    if await is_registered(db, event_id, user.id):
        raise ValueError("ALREADY_REGISTERED")
    reg = Registration(event_id=event_id, user_id=user.id)
    db.add(reg)
    await db.commit()
    await db.refresh(user)
    return user

async def list_attendees(db: AsyncSession, event_id: int, page: int, page_size: int) -> Tuple[int, List[User]]:
    statement: Select = select(func.count(Registration.id)).where(Registration.event_id == event_id)
    total_res = await db.exec(statement)
    total = int(total_res.one())
    offset = (page - 1) * page_size
    q = (
        select(User)
        .join(Registration, and_(Registration.user_id == User.id))
        .where(Registration.event_id == event_id)
        .order_by(User.id.asc())
        .offset(offset)
        .limit(page_size)
    )
    res = await db.exec(q)
    items = list(res.all())
    return total, items
