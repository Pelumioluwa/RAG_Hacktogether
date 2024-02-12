#connect AI search with Cosmos DB
import ai_search
import ingest
from dotenv import dotenv_values
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.models import Vector
from azure.search.documents.indexes.models import (
    IndexingSchedule,
    SearchIndex,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchField,
    SearchFieldDataType,
    SearchableField,
    SemanticConfiguration,
    SimpleField,
    PrioritizedFields,
    SemanticField,
    SemanticSettings,
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    SearchIndexerDataSourceConnection
)
from tenacity import retry, wait_random_exponential, stop_after_attempt
import json

#import AI search db credentials 
config = dotenv_values('credentials.env')

cog_search_endpoint = config['cog_search_endpoint']
cog_search_key = config['cog_search_key']
cosmosdb_connection_str_database = config['cosmosdb_connection_str_database']



def create_datasource():
    ds_client = SearchIndexerClient(cog_search_endpoint,ai_search.cog_search_cred)
    container = SearchIndexerDataContainer(name="CourseMaterials")
    datasource_connection = SearchIndexerDataSourceConnection(name='coursematerial-indexer', type='cosmosdb',
                                                              connection_string=cosmosdb_connection_str_database, container=container)
    datasource = ds_client.create_or_update_data_source_connection(datasource_connection)
    return datasource

ds_name = create_datasource().name
print(ds_name)


indexer = SearchIndexer(
        name="coursematerial-indexer",
        data_source_name=ds_name,
        target_index_name=ai_search.index_name)

indexer_client = SearchIndexerClient(cog_search_endpoint,ai_search.cog_search_cred)
indexer_client.create_or_update_indexer(indexer)  

result = indexer_client.get_indexer("coursematerial-indexer")
print(result)

# Run created indexer
indexer_client.run_indexer(result.name)

indexer_client.run_indexer('coursematerial-indexer')

#conduct a vector search 
def vector_search(query):
    searchclient = SearchClient(endpoint=cog_search_endpoint, index_name=ai_search.index_name, credential=ai_search.cog_search_cred)
    result = searchclient.search(search_text="",vector=Vector(value=ingest.generate_embeddings(query), k=3, fields='ContentEmbedding'),
                                 select=["BookTitle", "Content", "Course"])
    return result

query = 'calculate present values'
results = vector_search(query)
for result in results:
    print(f'The content is: {result["Content"]}')

