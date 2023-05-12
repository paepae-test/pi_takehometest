import asyncio
import sys
from fastapi import FastAPI

import app.api.user
from app.db.base import Base, engine


main_app = FastAPI()

main_app.include_router(app.api.user.router)


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if not "pytest" in sys.modules:
    asyncio.create_task(async_main())
