import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

import app.db.services as db_services
import app.db.models.user as user_models
import app.schemas.user as user_schema

from app.core.security import get_current_active_app_user
from app.db.models.app_user import AppUser
from app.db.base import async_session


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}", response_model=user_schema.User)
async def get_user(user_id: int, current_app_user: Annotated[AppUser, Depends(get_current_active_app_user)]):
    user = await db_services.UserService.get_user_async(async_session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.post("/", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, current_app_user: Annotated[AppUser, Depends(get_current_active_app_user)]):
    model_user = user_models.User(**user.dict())
    model_user.created_at = datetime.datetime.utcnow()
    model_user.updated_at = datetime.datetime.utcnow()
    model_user_id = await db_services.UserService.add_user_async(async_session, user=model_user)

    if model_user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    model_user.id = model_user_id
    return model_user


@router.put("/{user_id}", response_model=user_schema.User)
async def update_user(user_id: int, user: user_schema.UserUpdate, current_app_user: Annotated[AppUser, Depends(get_current_active_app_user)]):
    model_user = await db_services.UserService.get_user_async(async_session, user_id=user_id)
    if model_user is None:
        raise HTTPException(status_code=404)

    model_user.name = user.name
    model_user.email = user.email
    model_user.updated_at = datetime.datetime.utcnow()
    result = await db_services.UserService.update_user_async(async_session, user=model_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return model_user


@router.get("/", response_model=list[user_schema.User])
async def search_users_by_name(name: str, current_app_user: Annotated[AppUser, Depends(get_current_active_app_user)]):
    if len(name) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    users = await db_services.UserService.search_users_by_name_async(async_session, name=name)
    if users is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return users
