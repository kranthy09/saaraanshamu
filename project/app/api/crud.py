"""
CRUD operations on Database models
"""

from typing import Union

from app.models.tortoise import AppUser
from app.models.pydantic import UserIndb


async def get_user(username: str) -> Union[dict, None]:
    """Return user by username"""
    user = await AppUser.filter(username=username).first().values()
    if user:
        return UserIndb(**user)
    return None
