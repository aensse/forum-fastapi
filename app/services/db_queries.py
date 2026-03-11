from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import models
from app.db import AsyncSessionLocal
from app.schemas import PostEdit, PostRead, UserCreate, UserEdit


class UserQuery:
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


class PostQuery:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[models.Post]:
        stmt = select(models.Post).options(selectinload(models.Post.author))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_user_posts(self, user_id: int) -> list[models.Post]:
        stmt = select(models.Post).options(selectinload(models.Post.author)).where(models.Post.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_post_id(self, post_id: int) -> models.Post | None:
        stmt = select(models.Post).options(selectinload(models.Post.author)).where(models.Post.id == post_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, post: PostRead) -> models.Post:
        new_post = models.Post(
            title = post.title,
            content = post.content,
            user_id = post.user_id,
        )
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post, attribute_names=["author"])
        return new_post

    async def edit(self, post_obj: models.Post, post_edit: PostEdit) -> models.Post:
        update_data = post_edit.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post_obj, field, value)
        await self.db.commit()
        await self.db.refresh(post_obj, attribute_names=["author"])
        return post_obj

    async def delete(self, post: models.Post) -> None:
        await self.db.delete(post)
        await self.db.commit()


async def get_user_query():
    session = AsyncSessionLocal()
    try:
        yield UserQuery(session)
    finally:
        await session.close()

async def get_post_query():
    session = AsyncSessionLocal()
    try:
        yield PostQuery(session)
    finally:
        await session.close()






