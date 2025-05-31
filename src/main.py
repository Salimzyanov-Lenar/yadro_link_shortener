from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import Base, engine
from src.config import settings

from src.users.routers import router as users_router
from src.link_shortener.routers import router as links_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan, debug=settings.DEBUG)


@app.get("/health/")
async def health_check():
    return {"message": "OK"}


# Routers

# example.org/users/..
app.include_router(users_router)

# example.org/links/..
app.include_router(links_router)
