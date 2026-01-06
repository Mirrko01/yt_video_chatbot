import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    This class is used for environment configurations.
    """
    arbitrary_types_allowed = True

    # API ENVIROMENT variables
    IP: str = os.environ.get('IP', default="127.0.0.1")
    PORT: int = int(os.environ.get('PORT', default=5000))
    PREFIX: str = os.environ.get('PREFIX')
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY')
    KMP_DUPLICATE_LIB_OK: bool = os.environ.get('KMP_DUPLICATE_LIB_OK')


settings = Settings()
