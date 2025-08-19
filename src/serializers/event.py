from pydantic import BaseModel
from datetime import datetime

class EventPostSerializer(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int



class EventGetSerializer(EventPostSerializer):
    id: int

    class Config:
        orm_mode = True