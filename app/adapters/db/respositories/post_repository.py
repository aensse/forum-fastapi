from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.db import models
from app.api.dto import PostEdit, PostRead


class PostsDB:
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
