from pydantic_settings import BaseSettings

#Конфигурация подключения к базе данных
class ConfigDataBase(BaseSettings):
    SQLITE_DB_PATH: str = "app.db"
    DB_ECHO_LOG: bool = False

    #sqlite с использованием асинхронного драйвера aiosqlite
    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///src/{self.SQLITE_DB_PATH}" 

settings_db = ConfigDataBase()