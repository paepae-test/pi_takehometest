import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Optional

import app.db.models.app_user as app_user_models
import app.db.models.user as user_models


class UserService:

    @staticmethod
    async def get_user_async(async_session: async_sessionmaker[AsyncSession], user_id: int) -> user_models.User:
        async with async_session() as session:
            try:
                stmt = sa.text(f'SELECT * FROM "{user_models.User.__tablename__}" WHERE id=:user_id')
                result = await session.execute(
                    sa.select(user_models.User).from_statement(stmt),
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
    async def add_user_async(async_session: async_sessionmaker[AsyncSession], user: user_models.User) -> Optional[int]:
        async with async_session() as session:
            try:
                stmt = sa.text(f'INSERT INTO "{user_models.User.__tablename__}" (created_at, updated_at, name, email) VALUES (:created_at, :updated_at, :name, :email) RETURNING id')
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
    async def update_user_async(async_session: async_sessionmaker[AsyncSession], user: user_models.User) -> bool:
        async with async_session() as session:
            try:
                stmt = sa.text(f'UPDATE "{user_models.User.__tablename__}" SET updated_at=:updated_at, name=:name, email=:email WHERE id=:id')
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
    async def search_users_by_name_async(async_session: async_sessionmaker[AsyncSession], name: str) -> Optional[list[user_models.User]]:
        async with async_session() as session:
            try:
                stmt = sa.text(f'SELECT * FROM "{user_models.User.__tablename__}" WHERE name LIKE :name')
                result = await session.execute(
                    sa.select(user_models.User).from_statement(stmt),
                    {
                        "name": f"%{name}%",
                    },
                )
                users = result.scalars().all()
                return users
            except Exception as exc:
                print("UserService.search_user_by_name_async():", type(exc), exc)
                return None


class AppUserService:

    @staticmethod
    async def get_app_user_by_username_async(async_session: async_sessionmaker[AsyncSession], username: str) -> app_user_models.AppUser:
        async with async_session() as session:
            try:
                stmt = sa.text(f'SELECT * FROM "{app_user_models.AppUser.__tablename__}" WHERE username=:username')
                result = await session.execute(
                    sa.select(app_user_models.AppUser).from_statement(stmt),
                    {
                        "username": username,
                    },
                )
                app_user = result.scalars().one()
                return app_user
            except Exception as exc:
                print("AppUserService.get_app_user_by_username_async():", type(exc), exc)
                return None


    @staticmethod
    async def get_app_user_by_id_async(async_session: async_sessionmaker[AsyncSession], id: str) -> app_user_models.AppUser:
        async with async_session() as session:
            try:
                stmt = sa.text(f'SELECT * FROM "{app_user_models.AppUser.__tablename__}" WHERE id=:id')
                result = await session.execute(
                    sa.select(app_user_models.AppUser).from_statement(stmt),
                    {
                        "id": id,
                    },
                )
                app_user = result.scalars().one()
                return app_user
            except Exception as exc:
                print("AppUserService.get_app_user_by_id_async():", type(exc), exc)
                return None


    @staticmethod
    async def add_app_user_async(async_session: async_sessionmaker[AsyncSession], app_user: app_user_models.AppUser) -> Optional[int]:
        async with async_session() as session:
            try:
                stmt = sa.text(f'INSERT INTO "{app_user_models.AppUser.__tablename__}" (created_at, updated_at, is_active, username, password) VALUES (:created_at, :updated_at, :is_active, :username, :password) RETURNING id')
                result = await session.execute(
                    stmt,
                    {
                        "created_at": app_user.created_at,
                        "updated_at": app_user.updated_at,
                        "is_active": app_user.is_active,
                        "username": app_user.username,
                        "password": app_user.password,
                    },
                )
                await session.commit()
                for r in result:
                    return r[0]
                return None
            except Exception as exc:
                print("AppUserService.add_app_user_async():", type(exc), exc)
                return None
