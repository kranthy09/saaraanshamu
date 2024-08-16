"""
Utility helpers for API endpoints
"""

from datetime import datetime, timedelta
from typing import Union
import logging

import jwt

from argon2 import PasswordHasher

from app.api import crud

log = logging.getLogger("uvicorn")


ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ph = PasswordHasher()


def verify_password(plain_password, hashed_password):
    """Verify password using PasswordHasher"""
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception as err:
        print(f"Error: {err}")
        return False


async def authenticate_user(username: str, password: str) -> Union[dict, bool]:
    """Authenticate user with username and password"""

    user = await crud.get_user(username)
    print(f"user: {user}")

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a new access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
