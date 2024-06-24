from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import os
import certifi

from fastapi.middleware.cors import CORSMiddleware

from services.genai import (
    YoutubeProcessor,
    GeminiProcessor
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

genai_processor = GeminiProcessor(
        model_name="gemini-pro",
        project="mission-dynamo-426221"
    )

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisReq):
    # Analysis here

    

    processor = YoutubeProcessor(genai_processor = genai_processor)
    result = processor.retrieve_youtube_documents(str(request.youtube_link), verbose=True)

    

    #summary = genai_processor.generate_document_summary(result, verbose=True)

    # find key concepts
    key_concepts = processor.find_key_concepts(result, verbose=True)

    return {
       "key_concepts": key_concepts
    }
