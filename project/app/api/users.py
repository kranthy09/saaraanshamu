"""
Users API
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.models.pydantic import Token
from app.models.tortoise import AppUser


ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """Returns access token for user to login"""
    # continue by writing inside functions and run tests to pass for 200 success code.
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=None)
async def read_user_me(
    current_user: Annotated[AppUser, Depends(get_current_active_user)]
):
    """Return cuurent user"""

    return current_user
