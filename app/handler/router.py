from fastapi import APIRouter

from app.handler.ping.ping import router as ping_router
from app.handler.user.login import router as login_router


api_router = APIRouter()
api_router.include_router(ping_router)
api_router.include_router(login_router)

