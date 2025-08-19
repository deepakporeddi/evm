from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from evm.src.serializers.event import EventGetSerializer, EventPostSerializer
from evm.src.services.event_service import create_new_event, get_upcoming_events

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventGetSerializer)
async def create_event(event: EventPostSerializer, db: AsyncSession = Depends(get_db)):
    return await create_new_event(event, db=db)

@router.get("/", response_model=[EventGetSerializer])
async def get_events(db:AsyncSession = Depends(get_db)):
    return await get_upcoming_events(db)