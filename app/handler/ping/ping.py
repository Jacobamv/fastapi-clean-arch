import logging

from fastapi import APIRouter

from app.service.ping.pingService import ping_service


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/ping", summary="Health check")
def ping() -> dict[str, str]:
    logger.info("Processing /ping request")
    response = ping_service()
    logger.debug("Ping response generated", extra={"response": response})
    return response

