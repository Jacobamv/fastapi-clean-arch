from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.core.middleware import PanicCatcherMiddleware
from app.handler.router import api_router


settings = get_settings()
configure_logging(settings)
app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
)

app.add_middleware(PanicCatcherMiddleware)
app.include_router(api_router)

