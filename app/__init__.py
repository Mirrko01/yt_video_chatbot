import os
import yaml
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.api_settings import get_api_settings

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from config import settings

get_api_settings.cache_clear()
app_settings = get_api_settings()
app = FastAPI(**app_settings.fastapi_kwargs)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

from app.routers import video_chatbot_router

# Added router to the API
app.include_router(video_chatbot_router.router)

video_transcription_path = "C:/Users/mirko.contini/git/tirocinio-video-rag/resources/transcripions_dictionaries/6X58aP7yXC4.json"

try:
    llm = ChatOpenAI(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        model_name="gpt-3.5-turbo"
    )

    embeddings = OpenAIEmbeddings()
    empty_document = Document(
        page_content="",
    )

    vectorDB = FAISS.from_documents([empty_document], embeddings)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
