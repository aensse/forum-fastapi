## Scalable FastAPI Forum
> A project with an architecture of simple, online social forum. 
> The main goal is to understand real-world backend -> frontend communication and full-stack flow.


## API
Currently focused on a clean, fully RESTful API.

### Users
- POST /api/v1/users -> create new user
- POST /api/v1/users/token -> obtain access token (OAuth2 Password Flow + JWT)
- POST /api/v1/users/me -> get current user
- GET /api/v1/users/{user_id} -> get user by id
- PATCH /api/v1/users/{user_id} -> edit user
- DELETE /api/v1/users/{user_id} -> delete user
- GET /api/v1/users/{user_id}/posts -> get user posts

### Posts
- GET /api/v1/posts -> get all posts
- POST /api/v1/posts -> create post
- GET /api/v1/posts/{post_id} -> get post
- PATCH /api/v1/posts/{post_id} -> edit post
- DELETE -> /api/v1/posts/{post_id} -> delete post

## Tech behind
Application is asynchronous and built on top of [FastAPI](https://github.com/fastapi/fastapi).

A key components looks like so:
- I/O validation with [Pydantic](https://github.com/pydantic/pydantic) models,
- relational database with [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (via aiosqlite async driver),
- password hashing with Argon2 + JWT-based authentication (OAuth2).
- server-side HTML rendering with Jinja2 templates (basic frontend),
- super-simple HTML with CSS.

## Quick start
If you want to check the project on your machine follow instructions below.

I strongly recommend using [uv](https://docs.astral.sh/uv/), as further steps will be based on this package manager.

1) In the OS console (assuming you are in the folder where you want to keep the project), type:
```
git clone https://github.com/aensse/forum-fastapi
cd forum-fastapi
uv sync
cp .env-example .env
```

2) Generate a random 32-character string and fill .env with that variable (it will be a password for JWT tokens):
```
python3 -c "import secrets; print(secrets.token_hex(32))
```
- xAI API key – get one [here](https://console.x.ai/)
- Instagram credentials - just a data for a Instagram account

3) Run the server:
```
uv run fastapi dev
```










