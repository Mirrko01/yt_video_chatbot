import logging
from pydantic import BaseModel, validator
from typing import Optional, List, Union
from config import Settings

settings = Settings()

# getting logger configuration
logger = logging.getLogger(__name__)


class VideoUrlValidatorPayload(BaseModel):
    video_url: str

    @validator('video_url', pre=True)
    def video_url_val(cls, v):
        if v is not None and not isinstance(v, str):
            raise TypeError("video_url must be str, not " + type(v).__name__)
        return v
