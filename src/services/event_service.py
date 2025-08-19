from evm.src.models.event import Event
from evm.src.serializers.event import EventPostSerializer
from sqlalchemy.ext.asyncio import AsyncSession


async def create_new_event(event_data: EventPostSerializer, db: AsyncSession):
    event = Event(**event_data.model_dump())
    event.start_time = to_utc(event.start_time)
    event.end_time = to_utc(event.end_time)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def get_upcoming_events(db: AsyncSession):
    pass

