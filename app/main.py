from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.templating import Jinja2Templates

from app.api.v1 import posts, user
from app.db import Base, engine

templates = Jinja2Templates(directory="../templates")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )

app.include_router(router=user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(router=posts.router, prefix="/api/v1/posts", tags=["posts"])

@app.exception_handler(StarletteHTTPException)
async def general_http_exceptions_handler(request: Request, exception: StarletteHTTPException):
    return await http_exception_handler(request, exception)

@app.exception_handler(RequestValidationError)
async def validation_exceptions_handler(request: Request, exception: RequestValidationError):
    return await request_validation_exception_handler(request, exception)

