"""
Utility helpers for API endpoints
"""

from datetime import datetime, timedelta
from typing import Union, Annotated
import logging

import jwt

from argon2 import PasswordHasher
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.pydantic import TokenData
from app.models.tortoise import AppUser

from app.api import crud

log = logging.getLogger("uvicorn")


ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ph = PasswordHasher()


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


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


async def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    """Get the user in database with given token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await crud.get_user(username=token_data.username)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[
        AppUser,
        Depends(get_current_user),
    ]
):
    """Return the user if user is active"""

    if current_user.disabled:
        raise HTTPException(status_code=400, detail="User is disabled")
    return current_user
