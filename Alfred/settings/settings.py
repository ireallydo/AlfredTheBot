from pydantic import BaseSettings, Field
from pathlib import Path


class Settings(BaseSettings):

    TG_TOKEN: str = Field(..., env="TG_TOKEN")

    LOG_FILEPATH: str = Field("logs/app_log.log", env="LOG_FILEPATH")
    LOG_ROTATION: int = Field(1, env="LOG_ROTATION")
    LOG_RETENTION: int = Field(30, env="LOG_RETENTION")

    # media paths
    VOICE_RESP_mp3: str = Field("media/voice_resp.mp3", env="LOG_FILEPATH")
    VOICE_RESP_ogg: str = Field("media/voice_resp.ogg", env="LOG_FILEPATH")
    VOICE_REQ_wav: str = Field("media/voice_req.wav", env="LOG_FILEPATH")
    VOICE_REQ_ogg: str = Field("media/voice_req.ogg", env="LOG_FILEPATH")

    class Config:
        env_file = Path(__file__).parents[1].joinpath(".env")
        env_file_encoding = "utf-8"
