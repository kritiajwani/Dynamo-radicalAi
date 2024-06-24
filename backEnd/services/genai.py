from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAI
from langchain.chains.summarize import load_summarize_chain
from vertexai.generative_models import GenerativeModel
from langchain.prompts import PromptTemplate
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiProcessor:
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
    
    def count_total_token(self, docs:list):
        temp_model = GenerativeModel("gemini-1.0-pro")
        total = 0
        logger.info("Count total billable characters...")
    

        for doc in tqdm(docs):
            total += temp_model.count_tokens(doc.page_content).total_billable_characters

        return total
        
    def get_model(self):
        return self.model
    
class YoutubeProcessor:
    # Retrieve the full transcript
    def __init__(self, genai_processor: GeminiProcessor):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 0
        )
        self.GeminiProcessor = genai_processor

    def retrieve_youtube_documents(self, video_url: str, verbose = False):
        loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=True)
        docs = loader.load()
        result = self.text_splitter.split_documents(docs)

        author = result[0].metadata['author']
        length = result[0].metadata['length']
        title = result[0].metadata['title']
        total_size = len(result)
        total_billable_characters = self.GeminiProcessor.count_total_token(result)

        if verbose :
           logger.info(f"{author}\n{length}\n{title}\n{total_size}\n{total_billable_characters}")
        return docs
    
    def find_key_concepts(self, documents:list, sample_size: int=0, verbose = False):
        #iterate through all documents of group Size N and find key concepts
        if sample_size > len(documents):
            raise ValueError("Group Size is larger than the number of documents")
        
        if sample_size == 0:
            sample_size = len(documents) // 5
            if verbose: logging.info("No sample Size specified. Setting number of Documensr per sample as  Sample_size {sample_size}")



        #find the nummber of documents in each group
        num_docs_per_group = len(documents) // sample_size + (len(documents) % sample_size > 0)

        #optimize sameple size given no input
       
        #check thresholds

        if num_docs_per_group >= 10:
            raise ValueError("Each group has more than 10 documents Increase smaple_size to reduce number of documents per group")
        
        elif num_docs_per_group > 5:
            logging.warn("Each group has more than 5 documents Increase smaple_size to reduce number of documents per group")


        #split the documents in chunks of size num_docs_per_group
        groups = [documents[i:i+num_docs_per_group] for i in range(0, len(documents), num_docs_per_group)]

        batch_concepts = []
        batch_cost = 0

        logger.info("Finding key concepts..")
        for group in tqdm(groups):
            #combine content of documents per group
            group_content = ""
            

            for doc in group:
                group_content += doc.page_content

            #prompt for finding concepts
            prompt = PromptTemplate(
                template = """
                Find and define key concepts or terms found in the text:
                {text}
                Responds in the following formast as string seperating each concept with a comma:
                "concept": "definition"
                """,
                input_variables= ["text"]
            )

            #create Chain
            chain = prompt | self.GeminiProcessor.model

            # Run chain

            output_concept = chain.invoke({"text": group_content})
            batch_concepts.append(output_concept)

            if verbose:
                total_input_char = len(group_content)
                total_input_cost = (total_input_char/1000) * 0.000125
                logging.info("Running chain on {len(group)} documents")
                logging.info(f"Total Input Char: {total_input_char}")
                logging.info(f"Total Input Cost: ${total_input_cost}")


                total_output_char = len(output_concept)
                total_output_cost = (total_output_char/1000) * 0.000375
                logging.info(f"Total Input Char: {total_output_char}")
                logging.info(f"Total Input Cost: ${total_output_cost}")

                batch_cost += total_input_cost + total_output_cost
                logging.info(f"Batch Cost: ${total_input_cost + total_output_cost}\n")

            logger.info("Total Analysis Cost ${batch_cost}")

        return batch_concepts