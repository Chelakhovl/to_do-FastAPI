from fastapi import FastAPI
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
