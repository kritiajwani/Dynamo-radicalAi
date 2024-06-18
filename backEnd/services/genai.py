from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAI
from langchain.chains.summarize import load_summarize_chain
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YoutubeProcessor:
    # Retrieve the full transcript
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 0
        )
    def retrieve_youtube_documents(self, video_url: str, verbose = False):
        loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=True)
        docs = loader.load()
        result = self.text_splitter.split_documents(docs)

        author = result[0].metadata['author']
        length = result[0].metadata['length']
        title = result[0].metadata['title']
        total_size = len(result)

        if verbose :
           logger.info(f"{author}\n{length}\n{title}\n{total_size}")
        return docs
class Geminiprocessor:
    def __init__(self, model_name, project):
            self.model = VertexAI(model_name=model_name, project=project)

    def generate_document_summary(self, documents : list, **args) :
        chain_type = "map_reduce" if len(documents) > 10 else "stuff"
        chain = load_summarize_chain(
            chain_type = chain_type,
            llm = self.model,
            **args
            )

        return chain.run(documents)