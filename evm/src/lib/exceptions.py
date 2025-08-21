class InternalServerException(Exception):
    """Exception raised due to any unexpected bug in code"""


class NotFoundException(Exception):
    """Exception raised when the resource is not found"""


class BadRequestException(Exception):
    """Exception raised when request payload is failed at validation"""
