""" This file is used to push the content of pdf files and
their respective vector embeddings to the cosmos db container."""


import ingest
from dotenv import dotenv_values
from azure.cosmos import CosmosClient,exceptions,PartitionKey
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

#import cosmos db credentials 
config = dotenv_values('credentials.env')

cosmosdb_endpoint = config['cosmosdb_endpoint']
cosmosdb_key = config['cosmosdb_key']
cosmosdb_connection_str = config['cosmosdb_connection_str']

#connect with cosmos db
client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)


#create database
try:
    database = client.create_database_if_not_exists(id='hacktogether_rag')
    print(f'Database with id "{database.id}" created')

except exceptions.CosmosResourceExistsError:
    print(f'Database with id "{database.id}" already exists')
#create container
try:
    container = database.create_container_if_not_exists(
        id='CourseMaterials',
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    print(f'Container with id "{container.id}" created')
except exceptions.CosmosResourceExistsError:
    print(f'Container with id "{container.id}" already exists')

def load_data_to_container(data):
    for item in data:
        try: 
            container.create_item(body=item)
        except exceptions.CosmosResourceExistsError:
            print(f'item: {item} exists in container')


#import textbook folder to cosmos db
#computer_science = ingest.context('Computer Science') 
#load_data_to_container(computer_science)

#calculus = ingest.context('Calculus')
#load_data_to_container(calculus)

#physics = ingest.context('Physics')
#load_data_to_container(physics)

#finance = ingest.context('Finance')
#load_data_to_container(finance)

