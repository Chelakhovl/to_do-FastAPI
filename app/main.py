from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api.task_router import router as task_router
from .core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
)


# Include routers
app.include_router(task_router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "message": f"{settings.app_name} is running",
        "debug": settings.debug,
        "database": settings.database_url,
    }


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """
    Handle ValueError exceptions globally.

    Converts ValueError (from service layer) into HTTP 400 or 404 responses.
    """
    message = str(exc)
    status_code = 404 if "not found" in message.lower() else 400
    return JSONResponse(status_code=status_code, content={"detail": message})
