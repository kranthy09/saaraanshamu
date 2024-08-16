"""
Application instance
"""

import os
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI

from tortoise.contrib.fastapi import RegisterTortoise

from app.api import ping, users

log = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """establishing db connnection with lifespan"""

    log.info("Starting up...")
    async with RegisterTortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        yield

        log.info("Shutting down...")


def create_application(eventhandler):
    """Helper function to create a application"""

    application = FastAPI(lifespan=eventhandler)

    application.include_router(ping.router)
    application.include_router(users.router)

    return application


app = create_application(eventhandler=lifespan)
