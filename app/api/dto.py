from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)]

class UserCreate(User):
    password: Annotated[str, Field(min_length=6, max_length=200)]
    email: EmailStr

class UserPublic(User):
    id: int
    created_at: datetime

class UserPrivate(User):
    id: int
    email: EmailStr
    created_at: datetime


class UserEdit(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)] | None = Field(default=None)
    password: Annotated[str, Field(min_length=6, max_length=200)] | None = Field(default=None)
    email: EmailStr | None = Field(default=None)


class Post(BaseModel):
    title: Annotated[str, Field(max_length=50)]
    content: str
    user_id: int

class PostCreate(Post):
    pass

class PostRead(Post):
    id: int
    created_at: datetime
    author: User

class PostEdit(BaseModel):
    title: Annotated[str, Field(max_length=50)] | None = Field(default=None)
    content: str | None = Field(default=None)
