from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app import models
from app.schemas import PostCreate, PostEdit, PostRead
from app.services.db_queries import PostQuery, UserQuery, get_post_query, get_user_query

router = APIRouter()

@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    user_db: Annotated[UserQuery, Depends(get_user_query)],
    post_db: Annotated[PostQuery, Depends(get_post_query)],
):
    if not await user_db.get_by_user_id(post.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return await post_db.create(post)

@router.get("", response_model=list[PostRead])
async def get_posts(db: Annotated[PostQuery, Depends(get_post_query)]):
    return await db.get_all()

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: Annotated[PostQuery, Depends(get_post_query)]):
    post: models.Post = await db.get_by_post_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post

@router.patch("/{post_id}", response_model=PostRead)
async def edit_post(post_id: int, post_edit: PostEdit, db: Annotated[PostQuery, Depends(get_post_query)]):
    post_obj: models.Post = await db.get_by_post_id(post_id)
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return await db.edit(post_obj, post_edit)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Annotated[PostQuery, Depends(get_post_query)]):
    post_obj: models.Post = await db.get_by_post_id(post_id)
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    await db.delete(post_obj)
