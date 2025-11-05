import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Здесь можно подключить БД, кеш, и т.д.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Пример простого эндпоинта
    @app.get("/")
    async def read_root():
        return {"message": "Hello, World!"}

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
