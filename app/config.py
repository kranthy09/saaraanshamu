"""
Application enviroment configuration variables
"""

import logging
from functools import lru_cache

from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """
    Settings configuration for different environments
    """

    environment: str = "dev"
    testing: bool = bool(0)


@lru_cache
def get_settings() -> BaseSettings:
    """
    Load configuration settings based on the environment
    """
    log.info("Loading config settings from the environment...")
    return Settings()
