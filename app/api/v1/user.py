from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.adapters.db import models
from app.adapters.db.respositories.post_repository import PostsDB
from app.adapters.db.respositories.user_repository import UsersDB
from app.adapters.security.auth import check_password, create_token, hash_password, verify_token
from app.api.deps import get_posts_db, get_users_db
from app.api.dto import PostRead, Token, UserCreate, UserEdit, UserPrivate, UserPublic

router = APIRouter()

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

UsersDBDep = Annotated[UsersDB, Depends(get_users_db)]
PostsDBDep = Annotated[PostsDB, Depends(get_posts_db)]
TokenDep = Annotated[str, Depends(oauth_2_scheme)]


@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: UsersDBDep):
    if await db.get_by_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    if await db.get_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    hashed_password = hash_password(user.password)

    return await db.create(user, hashed_password)


@router.post("/token", response_model=Token)
async def login_for_token(db: UsersDBDep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await db.get_by_username(form.username)
    if not user or not check_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user.")

    token = create_token({"sub": str(user.id)})

    return Token(access_token=token, token_type="Bearer")  # noqa: S106


@router.post("/me", response_model=UserPrivate)
async def get_current_user(db: UsersDBDep, token: TokenDep):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    return await db.get_by_user_id(user_id)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, db: UsersDBDep):
    user: models.User | None = await db.get_by_user_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")


@router.get("/{user_id}/posts", response_model=list[PostRead])
async def get_user_posts(user_id: int, user_db: UsersDBDep, post_db: PostsDBDep):
    if not await user_db.get_by_user_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return await post_db.get_user_posts(user_id)


@router.patch("/{user_id}", response_model=UserPrivate)
async def edit_user(user_id: int, user_edit: UserEdit, db: UsersDBDep):
    user_obj: models.User | None = await db.get_by_user_id(user_id)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if user_edit.username != user_obj.username and await db.get_by_username(user_edit.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that username already exists.")
    if user_edit.email != user_obj.email and await db.get_by_email(user_edit.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that email already exists.")

    return await db.edit(user_obj, user_edit)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: UsersDBDep):
    user: models.User | None = await db.get_by_user_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    await db.delete(user)

