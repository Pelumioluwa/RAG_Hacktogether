from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import dotenv_values
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
from azure.search.documents.indexes import SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List

#import credentials
config = dotenv_values('app/credentials.env')
cog_search_endpoint = config['cog_search_endpoint']
cog_search_key = config['cog_search_key']
cosmosdb_connection_str_database = config['cosmosdb_connection_str_database']

# openai_api_key = config["openai_api_key"]  
# os.environ["OPENAI_API_KEY"] = openai_api_key  

cog_search_cred = AzureKeyCredential(cog_search_key)
index_name = 'course-materials-index'

indexer_client = SearchIndexerClient(cog_search_endpoint,cog_search_cred)

result = indexer_client.get_indexer("coursematerial-indexer")

# Run created indexer
indexer_client.run_indexer(result.name)

#conduct a vector search
def generate_embeddings(text):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    embeddings = embedding_model.embed_query(text)
    return embeddings

def vector_search(query):
    searchclient = SearchClient(endpoint=cog_search_endpoint, index_name= index_name, credential=cog_search_cred)
    result = searchclient.search(search_text="",vector=Vector(value= generate_embeddings(query), k=3, fields='ContentEmbedding'),
                                 select=["BookTitle", "Content", "Course"])
    return result

#define custom retriever
class VectorSearchRetriever(BaseRetriever):
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # Call vector_search
        results = vector_search(query)
        # Convert the results to a list of Document objects
        docs = [Document(page_content=result["Content"]) for result in results]
        return docs
