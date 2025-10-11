from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    jwt_private_key_path: str
    jwt_public_key_path: str
    jwt_algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 10080 # 7 days
    max_upload_size_mb: int = 10
    db_host: str
    db_username: str
    db_password: str
    db_name: str
    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")

settings = Settings() # type: ignore
