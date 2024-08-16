"""
Pydantic models of the app.
"""

from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    url: str


class Token(BaseModel):
    """Response for user access token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data for user"""

    username: str = None
