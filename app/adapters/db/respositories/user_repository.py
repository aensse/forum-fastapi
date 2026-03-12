from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db import models
from app.api.dto import UserCreate, UserEdit


class UsersDB:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[models.User]:
        stmt = select(models.User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_user_id(self, user_id: int) -> models.User | None:
        stmt = select(models.User).where(models.User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_username(self, username: str) -> models.User | None:
        stmt = select(models.User).where(models.User.username == username)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> models.User | None:
        stmt = select(models.User).where(models.User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user: UserCreate, hashed_password: str) -> models.User:
        new_user = models.User(
            username = user.username,
            hashed_password = hashed_password,
            email = user.email,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def edit(self, user_obj: models.User, user_edit: UserEdit) -> models.User:
        update_data = user_edit.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_obj, field, value)
        await self.db.commit()
        await self.db.refresh(user_obj)
        return user_obj

    async def delete(self, user: models.User) -> None:
        await self.db.delete(user)
        await self.db.commit()








