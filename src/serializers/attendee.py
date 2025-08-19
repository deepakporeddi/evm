from pydantic import BaseModel, EmailStr

class AttendeePostSerializer(BaseModel):
    name: str
    email: EmailStr

class AttendeeGetSerializer(AttendeePostSerializer):
    id: int

    class Config:
        orm_mode = True