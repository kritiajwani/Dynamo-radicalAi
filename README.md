# GenAI Processor and YouTube Processor

## Overview

This repository contains a FastAPI application for processing YouTube video transcripts and generating summaries and key concepts using the VertexAI model. The main components include:

- **GenAIProcessor**: A class for generating document summaries and counting billable tokens.
- **YoutubeProcessor**: A class for retrieving YouTube video transcripts, splitting text, and finding key concepts.

## Dependencies

- `fastapi`: Web framework for building APIs.
- `pydantic`: Data validation and settings management.
- `langchain_community`: Community extensions for LangChain.
- `langchain_google_vertexai`: LangChain integration with Google Vertex AI.
- `tqdm`: Progress bar for loops.
- `json`: JSON parsing.

## Setup

1. **Install Dependencies**:
  Google Cloud Authentication: Ensure you have a valid Google Cloud credentials file and set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the credentials file:
bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'
# Usage
**GenAIProcessor**
The GenAIProcessor class is used for generating document summaries and counting billable tokens.
genai_processor = GenAIProcessor(model_name="your-model-name", project="your-project-id")

**Generate Document Summary:**
summary = genai_processor.generate_document_summary(documents_list)

**Count Billable Tokens:**
token_count = genai_processor.count_billable_tokens(documents_list)

**YoutubeProcessor**
The YoutubeProcessor class is used for retrieving YouTube video transcripts, splitting text, and finding key concepts.

**Initialization:**
youtube_processor = YoutubeProcessor(genai_processor)

**Retrieve YouTube Documents:**
documents = youtube_processor.retrieve_youtube_documents(video_url="https://youtube.com/your-video-url", verbose=True)

**Find Key Concepts:**
key_concepts = youtube_processor.find_key_concepts(documents_list, sample_size=10, verbose=True)

**Configuration**
Environment Variable: Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to authenticate Google Cloud services.

**Logging**
The application uses the logging module to provide insights into its operations. You can configure logging level and handlers as needed.


