import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from minio import Minio

from api.routes import router
from core.config import Config
from db.base import async_pg_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения.
    Выполняет инициализацию при запуске и очистку при завершении.
    """
    logger.info("Инициализация PostgreSQL...")
    engine = async_pg_engine
    app.state.db_engine = engine
    logger.info("Запущен PostgreSQL")

    logger.info("Инициализация Minio...")
    minio_client = Minio(
        f"{Config.minio_config.MINIO_HOST}:{Config.minio_config.MINIO_PORT}",
        access_key=Config.minio_config.MINIO_USER,
        secret_key=Config.minio_config.MINIO_PASSWORD,
        secure=False,
    )
    if not minio_client.bucket_exists(Config.minio_config.MINIO_BUCKET):
        minio_client.make_bucket(Config.minio_config.MINIO_BUCKET)
        logger.info(f"Создан бакет для Minio : {Config.minio_config.MINIO_BUCKET}")
    app.state.minio_client = minio_client
    logger.info("Запущен Minio")

    yield

    await engine.dispose()


app = FastAPI(
    title="MyBeacon API",
    description="API для управления работой приложения",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


app.include_router(router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


def start():
    """Запуск FastAPI сервера"""
    port = int(Config.app_config.PORT)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    start()
