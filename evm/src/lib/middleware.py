import json
import logging

from fastapi import Request

from evm.src.lib.exceptions import InternalServerException

logger = logging.getLogger()


def RequestLogMiddleware(request: Request, call_next):
    logger.info(
        f"Received request from {request.client}: {request.method} {request.url}"
    )

    # Prepare log details to be written
    log_details = {
        "method": request.method,
        "path": request.url.path if request.url else "unknown",
        "source_ip": request.client.host if request.client else "unknown",
        "params": dict(request.query_params),
    }

    # Log request details
    logger.info(f"Request Log Details:\n{json.dumps(log_details)}\n", extra=log_details)
    try:
        response = call_next(request)
        return response
    except Exception as e:
        logger.exception("An error occurred while processing the request", exc_info=e)
        raise InternalServerException(f"An error occurred while processing the request: {str(e)}")
