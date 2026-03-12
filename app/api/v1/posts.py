from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.adapters.db import models
from app.adapters.db.respositories.post_repository import PostsDB
from app.adapters.db.respositories.user_repository import UsersDB
from app.api.deps import get_posts_db, get_users_db
from app.api.dto import PostCreate, PostEdit, PostRead

router = APIRouter()

UsersDBDep = Annotated[UsersDB, Depends(get_users_db)]
PostsDBDep = Annotated[PostsDB, Depends(get_posts_db)]

@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, user_db: UsersDBDep, post_db: PostsDBDep):
    if not await user_db.get_by_user_id(post.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return await post_db.create(post)

@router.get("", response_model=list[PostRead])
async def get_posts(db: PostsDBDep):
    return await db.get_all()

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: PostsDBDep):
    post: models.Post = await db.get_by_post_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post

@router.patch("/{post_id}", response_model=PostRead)
async def edit_post(post_id: int, post_edit: PostEdit, db: PostsDBDep):
    post_obj: models.Post = await db.get_by_post_id(post_id)
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return await db.edit(post_obj, post_edit)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: PostsDBDep):
    post_obj: models.Post = await db.get_by_post_id(post_id)
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    await db.delete(post_obj)
