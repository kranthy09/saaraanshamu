"""
Pydantic models of the app.
"""

from datetime import datetime
from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    """payload for url summary endpoint"""

    url: str


class Token(BaseModel):
    """Response for user access token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data for user"""

    username: str = None


class UserIndb(BaseModel):
    """User representation in db"""

    username: str
    hashed_password: str = None
    created_at: datetime = None
