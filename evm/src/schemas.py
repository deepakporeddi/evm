from __future__ import annotations
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List
from datetime import datetime

from evm.src.lib.exceptions import BadRequestException


class ErrorResponse(BaseModel):
    Detail: str


class EventCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)
    start_time: datetime
    end_time: datetime
    max_capacity: int = Field(gt=0)

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, end_time: datetime, info):
        start_time = info.data.get("start_time")
        if start_time and end_time <= start_time:
            raise BadRequestException("end_time must be after start_time")
        return end_time

class EventGet(BaseModel):
    id: int
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    class Config:
        from_attributes = True

class AttendeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr

class AttendeeGet(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class PaginatedAttendees(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[AttendeeGet]
