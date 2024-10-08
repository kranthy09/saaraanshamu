"""
Reusable objects for Tests: Fixtures
"""

import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import RegisterTortoise

from app.main import create_application, lifespan
from app.config import get_settings, Settings


def get_settings_override():
    """Override the default settings"""

    return Settings(
        testing=1, database_url=os.environ.get("DATABASE_TEST_URL")
    )


@pytest.fixture(scope="module")
def test_app():
    """Test application instance"""

    # set up
    app = create_application(lifespan)
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    """Fixture for testing app with database"""
    app = create_application(lifespan)
    app.dependency_overrides[get_settings] = get_settings_override
    RegisterTortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down
