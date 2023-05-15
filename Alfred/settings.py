from pydantic import BaseSettings, Field
from pathlib import Path


class Settings(BaseSettings):

    TG_TOKEN: str = Field(..., env="TG_TOKEN")
    OPENAI_TOKEN: str = Field(..., env="OPENAI_TOKEN")

    LOG_FILEPATH: str = Field("logs/app_log.log", env="LOG_FILEPATH")
    LOG_ROTATION: int = Field(1, env="LOG_ROTATION")
    LOG_RETENTION: int = Field(30, env="LOG_RETENTION")

    class Config:
        env_file = Path(__file__).parents[1].joinpath(".env")
        env_file_encoding = "utf-8"
