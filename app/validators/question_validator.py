import logging
from pydantic import BaseModel, validator
from typing import Optional, List, Union
from config import Settings

settings = Settings()

# getting logger configuration
logger = logging.getLogger(__name__)


class QuestionValidatorPayload(BaseModel):
    question: str

    @validator('question', pre=True)
    def question_val(cls, v):
        if v is not None and not isinstance(v, str):
            raise TypeError("question must be str, not " + type(v).__name__)
        return v
