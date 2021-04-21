from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import ALGORITHM
from app.crud import users as crud_user
from app.schemas.token import TokenPayload

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_session():
    async with SessionLocal() as session:
        yield session


def get_token_data(token: str = Depends(oauth2)) -> TokenPayload:
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token_data


async def get_current_user(
    token: str = Depends(get_token_data),
    session: AsyncSession = Depends(get_session),
):
    user = await crud_user.get_user_by_id(session, id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user