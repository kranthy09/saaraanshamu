"""
Pydantic models of the app.
"""

from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    url: str
