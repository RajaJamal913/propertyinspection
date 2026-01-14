from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # keep default details but wrap in consistent object
        return Response({
            "message": "An error occurred",
            "detail": response.data,
            "success": False
        }, status=response.status_code)

    # Unhandled exceptions -> 500 with logging
    logger.exception("Unhandled Exception: %s", exc)
    return Response({
        "message": "Internal Server Error",
        "detail": str(exc),
        "success": False
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
