import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src import router
from src.config import settings
from src.services import initialize_database

#Вызов функции для создания БД с тестовыми данными
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

# Создание приложения
app = FastAPI(
    lifespan=lifespan,
    openapi_tags=settings.TAGS_METADATA
)

#Роутинг
app.include_router(router)

#Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)