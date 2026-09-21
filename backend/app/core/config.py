import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "QuantumShield"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/quantumshield.db")

    MAX_ZIP_SIZE_BYTES: int = 50 * 1024 * 1024          # 50 MB
    MAX_UNCOMPRESSED_SIZE_BYTES: int = 200 * 1024 * 1024  # 200 MB
    MAX_FILES_IN_ARCHIVE: int = 5000
    MAX_SINGLE_FILE_SIZE_BYTES: int = 10 * 1024 * 1024    # 10 MB

    UPLOAD_TMP_DIR: str = str(BASE_DIR / "tmp_uploads")
    REPORTS_DIR: str = str(BASE_DIR / "generated_reports")

    CORS_ORIGINS: list[str] = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://cryptoscan-livid.vercel.app",
]
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

os.makedirs(settings.UPLOAD_TMP_DIR, exist_ok=True)
os.makedirs(settings.REPORTS_DIR, exist_ok=True)
