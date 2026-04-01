import os

class Settings:
    PROJECT_NAME: str = "Finance Dashboard Backend"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey_for_assignment_only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

settings = Settings()
