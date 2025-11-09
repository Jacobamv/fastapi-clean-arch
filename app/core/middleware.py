import logging
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class PanicCatcherMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any):
        try:
            response = await call_next(request)
            return response
        except SQLAlchemyError as error:
            logger.exception(
                "Database error during request processing",
                extra={"path": request.url.path},
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": "database_error",
                        "message": "Database operation failed.",
                        "detail": str(error),
                    }
                },
            )
        except Exception as error:  # pragma: no cover - safeguard branch
            logger.exception(
                "Unhandled error during request processing",
                extra={"path": request.url.path},
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": "internal_error",
                        "message": "Unexpected server error.",
                        "detail": str(error),
                    }
                },
            )

