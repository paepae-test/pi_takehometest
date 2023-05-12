import asyncio
import datetime
import sys
from fastapi import FastAPI

import app.api.auth
import app.api.user
from app.core.security import get_password_hash
from app.db.base import async_session, Base, engine


main_app = FastAPI()

main_app.include_router(app.api.auth.router)
main_app.include_router(app.api.user.router)


async def create_test_app_user():
    from app.core.config import settings
    from app.db.services import AppUserService
    from app.db.models.app_user import AppUser

    # Check if test user exists
    username = settings.TEST_APP_USER_USERNAME
    app_user = await AppUserService.get_app_user_by_username_async(async_session, username)
    if app_user:
        return

    # Create test user
    hashed_password = get_password_hash(settings.TEST_APP_USER_PASSWORD)
    app_user_create = AppUser(
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
        is_active=True,
        username=username,
        password=hashed_password,
    )
    await AppUserService.add_app_user_async(async_session, app_user_create)


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await create_test_app_user()

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if not "pytest" in sys.modules:
    asyncio.create_task(async_main())
