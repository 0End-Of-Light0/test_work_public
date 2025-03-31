from typing import List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field

#Настройки API
class Settings(BaseSettings):
    DB_ECHO: bool = Field(True, description="Режим отладки SQL-запросов")
    PROJECT_NAME: str = Field("test_project", description="Название проекта")
    VERSION: str = Field("0.0.1", description="Версия приложения")
    DEBUG: bool = Field("True", description="Режим отладки")
    CORS_ALLOWED_ORIGINS: str = Field("ALL", description="Разрешенные домены для CORS")
    
    HOST: str = Field("0.0.0.0", description="Хост для запуска сервера")
    PORT: int = Field(8000, description="Порт для запуска сервера")

    LIMIT: int = Field(100, description="Ограничение на получение всех записей")
    
    TAGS_METADATA: List[Dict[str, Any]] = Field(
        [
            {
                "name": "person",
                "description": "Работа с конкретным человеком. Поиск осуществляется по Фамилии. "
                "Возвращает полную информацию о человеке включая связанные email-адреса. "
            },
            {
                "name": "people",
                "description": "Получение списка всех людей в базе данных"
            },
            {
                "name": "createperson",
                "description": "Создание новой записи о человеке с валидацией данных. "
            },
            {
                "name": "updateperson",
                "description": "Частичное обновление информации о человеке по его ID. "
            },
            {
                "name": "deleteperson",
                "description": "Удаляет человека  из БД. В запросе необходжимо указать Id"
            }
        ],
        description="Метаданные для группировки эндпоинтов в Swagger",
    )
    DEFAULT_PEOPLE_TEST: List[str] = Field(
        ["Зубова Валерия Максимовна", "Макеев Максим Матвеевич", "Соловьева Кира Ивановна", "Полякова Елизавета Егоровна", 
        "Одинцова Карина Ильинична", "Соколова Аглая Владимировна", "Пугачев Тимофей Васильевич", "Исаев Павел Егорович", "Кузнецов Михаил Артёмович", "Котов Марк Владиславович"],
        description="Список тестовых ФИО для инициализации БД"
    )
    DEFAULT_PEOPLE_TEST_API: List[str] = Field(
        ["Зубова Валерия Максимовна", "Макеев Максим Матвеевич"],
        description="Список тестовых ФИО для инициализации БД (Чтобы не нагружать API)"
    )
    
    DEFAULT_MAIL_TEST: List[List[str]] = Field(
        [["test1@mail.com", "test2@mail.com"], ["test3@mail.com"]],
        description="Список тестовых email-адресов для инициализации БД"
    )

settings = Settings()
