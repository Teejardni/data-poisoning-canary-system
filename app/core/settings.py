from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "TBD"
    redis_endpoint: str = "redis://localhost:6379/0"
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool = False 

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()