from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from app.api.routes import router as api_router
from app.core.config import get_settings
from app.core.logger import configure_logger


def create_application() -> FastAPI:
    """Application factory for FastAPI app."""

    settings = get_settings()
    configure_logger(settings.debug)

    app = FastAPI(title=settings.app_name)

    app.include_router(api_router)

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions globally."""
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    logger.info("Application initialized successfully")

    return app


app = create_application()