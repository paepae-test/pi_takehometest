from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Annotated

from app.core.config import settings
from app.db.base import async_session
from app.db.models.app_user import AppUser
from app.db.services import AppUserService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_app_user_async(username: str, password: str):
    app_user = await AppUserService.get_app_user_by_username_async(async_session, username)
    if not app_user:
        return None
    if not verify_password(password, app_user.password):
        return None
    return app_user


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_app_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        app_user_id = int(payload.get("sub"))
    except Exception as exc:
        print("get_current_app_user():", type(exc), exc)
        raise credentials_exception

    app_user = await AppUserService.get_app_user_by_id_async(async_session, app_user_id)
    if app_user is None:
        raise credentials_exception

    return app_user


async def get_current_active_app_user(current_user: Annotated[AppUser, Depends(get_current_app_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user
