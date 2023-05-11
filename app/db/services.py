import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Optional

import app.db.models.user as models_user


class UserService:

    @staticmethod
    async def get_user_async(async_session: async_sessionmaker[AsyncSession], user_id: int) -> models_user.User:
        async with async_session() as session:
            try:
                stmt = sa.text(f'SELECT * FROM "{models_user.User.__tablename__}" WHERE id=:user_id')
                result = await session.execute(
                    sa.select(models_user.User).from_statement(stmt),
                    {
                        "user_id": user_id
                    },
                )
                user = result.scalars().one()
                return user
            except Exception as exc:
                print("UserService.get_user_async():", type(exc), exc)
                return None


    @staticmethod
    async def add_user_async(async_session: async_sessionmaker[AsyncSession], user: models_user.User) -> Optional[int]:
        async with async_session() as session:
            try:
                stmt = sa.text(f'INSERT INTO "{models_user.User.__tablename__}" (created_at, updated_at, name, email) VALUES (:created_at, :updated_at, :name, :email) RETURNING id')
                result = await session.execute(
                    stmt,
                    {
                        "created_at": user.created_at,
                        "updated_at": user.updated_at,
                        "name": user.name,
                        "email": user.email,
                    },
                )
                await session.commit()
                for r in result:
                    return r[0]
                return None
            except Exception as exc:
                print("UserService.add_user_async():", type(exc), exc)
                return None


    @staticmethod
    async def update_user_async(async_session: async_sessionmaker[AsyncSession], user: models_user.User) -> bool:
        async with async_session() as session:
            try:
                stmt = sa.text(f'UPDATE "{models_user.User.__tablename__}" SET updated_at=:updated_at, name=:name, email=:email WHERE id=:id')
                await session.execute(
                    stmt,
                    {
                        "updated_at": user.updated_at,
                        "name": user.name,
                        "email": user.email,
                        "id": user.id,
                    },
                )
                await session.commit()
                return True
            except Exception as exc:
                print("UserService.update_user_async():", type(exc), exc)
                return False


    @staticmethod
    async def search_users_by_name_async(async_session: async_sessionmaker[AsyncSession], name: str) -> Optional[list[models_user.User]]:
        async with async_session() as session:
            try:
                stmt = sa.text(f'SELECT * FROM "{models_user.User.__tablename__}" WHERE name LIKE :name')
                result = await session.execute(
                    sa.select(models_user.User).from_statement(stmt),
                    {
                        "name": f"%{name}%",
                    },
                )
                users = result.scalars().all()
                return users
            except Exception as exc:
                print("UserService.search_user_by_name_async():", type(exc), exc)
                return None
