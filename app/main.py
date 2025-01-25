"""
This module initializes the main FastAPI application, registers the main router
and admin interface, and sets up any necessary resources (such as a superuser)
on application startup.
"""

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser
from app.admin import create_admin


app = FastAPI(
    title=settings.app_title,
    description=settings.description
)

# Include the main router with all defined endpoints
app.include_router(main_router)

# Create and configure the admin interface
create_admin(app)


@app.on_event('startup')
async def startup():
    """
    Event handler that runs when the application starts.

    Creates the first superuser in the database if none exists.
    """
    await create_first_superuser()
