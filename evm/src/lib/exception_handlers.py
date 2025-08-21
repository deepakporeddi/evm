import logging

from .exceptions import (
    BadRequestException,
    InternalServerException,
    NotFoundException,
)
from evm.src.schemas import ErrorResponse
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger()


def not_found_exception_handler(
    request: Request, exc: NotFoundException
) -> JSONResponse:
    logger.error(
        "Resource Error: %s details:  %s",
        status.HTTP_404_NOT_FOUND,
        str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(Detail=str(exc)).model_dump(),
    )


def internal_exception_handler(
    request: Request, exc: InternalServerException
) -> JSONResponse:
    logger.error(
        "Internal Server Error: %s details:  %s",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(Detail=str(exc)).model_dump(),
    )


def bad_request_exception_handler(
    request: Request, exc: BadRequestException
) -> JSONResponse:
    logger.error(
        "Bad Request Payload: %s details:  %s",
        status.HTTP_400_BAD_REQUEST,
        str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(Detail=str(exc)).model_dump(),
    )
