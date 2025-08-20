from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .lib.exception_handlers import internal_exception_handler, bad_request_exception_handler, \
    not_found_exception_handler
from .lib.exceptions import InternalServerException, BadRequestException, NotFoundException
from .lib.middleware import RequestLogMiddleware
from .routers import router

app = FastAPI(title="Event Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.openapi_version = "3.0.2"
app.add_exception_handler(InternalServerException, internal_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.middleware("http")(RequestLogMiddleware)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
