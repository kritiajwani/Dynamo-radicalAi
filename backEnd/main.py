from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import os
import certifi

from fastapi.middleware.cors import CORSMiddleware

from services.genai import (
    YoutubeProcessor,
    Geminiprocessor
)

# Ensure certifi's certificates are used
os.environ["SSL_CERT_FILE"] = certifi.where()

class VideoAnalysisReq(BaseModel):
    youtube_link: HttpUrl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisReq):
    # Analysis here
    processor = YoutubeProcessor()
    result = processor.retrieve_youtube_documents(str(request.youtube_link), verbose=True)

    genai_processor = Geminiprocessor(
        model_name="gemini-pro",
        project="mission-dynamo-426221"
    )

    summary = genai_processor.generate_document_summary(result, verbose=True)

    return {
       "summary": summary
    }
