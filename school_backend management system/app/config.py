import os
from dotenv import load_dotenv

load_dotenv()  # .env file se variables load karega


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "School Management Backend")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./school.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@school.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")


settings = Settings()
