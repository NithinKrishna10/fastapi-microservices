from typing import Optional, Any

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: Any


class TokenPayload(BaseModel):
    user_id: Optional[int]
