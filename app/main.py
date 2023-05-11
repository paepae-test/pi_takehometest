import asyncio
import datetime
from fastapi import FastAPI, HTTPException

import app.db.models.user as models_user
import app.db.services as db_service
import app.schemas.user as schemas_user
from app.core.config import settings
from app.db.base import async_session, Base, engine


app = FastAPI()


@app.get("/users/{user_id}", response_model=schemas_user.User)
async def get_user(user_id: int):
    user = await db_service.UserService.get_user_async(async_session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404)

    return user


@app.post("/users", response_model=schemas_user.User)
async def create_user(user: schemas_user.UserCreate):
    model_user = models_user.User(**user.dict())
    model_user.created_at = datetime.datetime.utcnow()
    model_user.updated_at = datetime.datetime.utcnow()
    model_user_id = await db_service.UserService.add_user_async(async_session, user=model_user)

    if model_user_id is None:
        raise HTTPException(status_code=400)

    model_user.id = model_user_id
    return model_user


@app.put("/users/{user_id}", response_model=schemas_user.User)
async def update_user(user_id: int, user: schemas_user.UserUpdate):
    model_user = await db_service.UserService.get_user_async(async_session, user_id=user_id)
    if model_user is None:
        raise HTTPException(status_code=404)

    model_user.name = user.name
    model_user.email = user.email
    model_user.updated_at = datetime.datetime.utcnow()
    result = await db_service.UserService.update_user_async(async_session, user=model_user)
    if not result:
        raise HTTPException(status_code=400)

    return model_user


@app.get("/users", response_model=list[schemas_user.User])
async def search_users_by_name(name: str):
    if len(name) == 0:
        raise HTTPException(status_code=400)

    users = await db_service.UserService.search_users_by_name_async(async_session, name=name)
    if users is None:
        raise HTTPException(status_code=500)

    return users


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


asyncio.create_task(async_main())
