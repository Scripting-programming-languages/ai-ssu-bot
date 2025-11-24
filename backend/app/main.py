import os

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
from qdrant_client import QdrantClient

from upd_qdrant import update_qdrant

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

qdrant_client: QdrantClient | None = None

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Здесь можно подключить БД, кеш, и т.д.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global qdrant_client

    try:
        qdrant_client = QdrantClient(host=os.environ["QDRANT_HOST"], port=os.environ["QDRANT_PORT"])
        logger.info("Connected to Qdrant")
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")

    yield

    if qdrant_client:
        qdrant_client = None
        logger.info("Qdrant client closed")


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
    
    @app.get("/qdrant-check")
    async def qdrant_check():
        info = qdrant_client.get_collections()
        return {"qdrant_collections": info.model_dump()}
    
    @app.post("/update-qdrant")
    async def update_qdrant_endpoint():
        global qdrant_client
        if not qdrant_client:
            return {"error": "Qdrant client is not initialized"}

        result = await asyncio.to_thread(update_qdrant, qdrant_client)
        return result

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
