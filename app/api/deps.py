from app.adapters.db.respositories.post_repository import PostsDB
from app.adapters.db.respositories.user_repository import UsersDB
from app.adapters.db.session import AsyncSessionLocal


async def get_users_db():
    session = AsyncSessionLocal()
    try:
        yield UsersDB(session)
    finally:
        await session.close()

async def get_posts_db():
    session = AsyncSessionLocal()
    try:
        yield PostsDB(session)
    finally:
        await session.close()
