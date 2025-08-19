from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/events", tags=["attendee"])

@router.post("/{event_id}/register")
async def register_attendee():
    pass


@router.get("/{event_id}/attendees")
async def get_attendee():
    pass