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

#using Azure AI Search
#creating an index
cog_search_cred = AzureKeyCredential(cog_search_key)
index_name = 'course-materials-index'

#defining schema
index_client = SearchIndexClient(endpoint=cog_search_endpoint, credential=cog_search_cred)
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="BookTitle", type=SearchFieldDataType.String,
                    searchable=True, retrievable=True),
    SearchableField(name="Content", type=SearchFieldDataType.String,
                    searchable=True, retrievable=True),
    SearchableField(name="Course", type=SearchFieldDataType.String,
                    filterable=True, searchable=True, retrievable=True),
    SearchField(name="TitleEmbedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True, dimensions=768, vector_search_configuration="vector-config"),
    SearchField(name="ContentEmbedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True, dimensions=768, vector_search_configuration="vector-config"),

]
#configure vector search
vector_search = VectorSearch(
    algorithm_configurations=[
        VectorSearchAlgorithmConfiguration(
            name="vector-config", 
            kind="hnsw",
            hnsw_parameters={
                "m": 4,
                "efConstruction": 400,
                "efSearch": 1000,
                "metric": "cosine"
            })])

# Configure semantic search. 
semantic_config = SemanticConfiguration(
    name="my-semantic-config",
    prioritized_fields=PrioritizedFields(
        title_field=SemanticField(field_name="BookTitle"),
        prioritized_keywords_fields=[SemanticField(field_name="Course")],
        prioritized_content_fields=[SemanticField(field_name="Content")],
       )
)

# Create the semantic settings with the configuration
semantic_settings = SemanticSettings(configurations=[semantic_config])

# Create the search index with the semantic settings
index = SearchIndex(name=index_name, fields=fields,
                    vector_search=vector_search, semantic_settings=semantic_settings)
result = index_client.create_or_update_index(index)
print(f' {result.name} created')

