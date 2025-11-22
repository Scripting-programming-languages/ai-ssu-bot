import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.core.database import database, metadata
from app.core.config import settings
from app.api import ssu_bot_api
from app.api import health_api

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Здесь можно подключить БД, кеш, и т.д.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Выполняем рефлексию базы данных
    async with database.engine.begin() as conn:
        await conn.run_sync(metadata.reflect, views=True)
    yield


def create_app() -> FastAPI:
    app_options = {}
    app = FastAPI(lifespan=lifespan, root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(ssu_bot_api.router)
    app.include_router(health_api.router)

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
