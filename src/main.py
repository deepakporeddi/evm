from fastapi import FastAPI
from evm.src.api import attendee
from evm.src.api import event

app = FastAPI(title="Event Management System")

app.include_router(event.router)
app.include_router(attendee.router)