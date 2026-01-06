from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, FastAPI, BackgroundTasks

import logging
import time

# SETTINGS:
from config import settings

# PIPELINES
from app.core.pipelines import load_video_pipeline, ask_pipeline

# VALIDATOR
from app.validators.video_url_validator import VideoUrlValidatorPayload
from app.validators.question_validator import QuestionValidatorPayload

# Logger configuration
logger = logging.getLogger(__name__)

router = APIRouter(prefix=f"{settings.PREFIX}", tags=["load_video"])
app = FastAPI(debug=True)


################
# HEALTH CHECK #
################


@router.get('/status')
async def health_check():
    return JSONResponse(content={'Status': 'Available'},
                        status_code=200)


@router.post('/load_video')
async def ask(item: VideoUrlValidatorPayload) -> JSONResponse:
    try:
        request_json = item.dict()
        logger.info(f"Starting answer generation...")
        start = time.time()
        answer = load_video_pipeline.load(request_json)
        logger.info(f"Answer generation successfully completed in {round(time.time() - start, 1)} sec")

        return JSONResponse(content={"answer": answer},
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"ERROR in answer generation", exc_info=e)
        return JSONResponse(content={"status": "ERROR in answer generation"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/ask')
async def ask(item: QuestionValidatorPayload) -> JSONResponse:
    try:
        request_json = item.dict()
        logger.info(f"Starting answer generation...")
        start = time.time()
        answer = ask_pipeline.ask(request_json)
        logger.info(f"Answer generation successfully completed in {round(time.time() - start, 1)} sec")

        return JSONResponse(content={"answer": answer},
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"ERROR in answer generation", exc_info=e)
        return JSONResponse(content={"status": "ERROR in answer generation"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
