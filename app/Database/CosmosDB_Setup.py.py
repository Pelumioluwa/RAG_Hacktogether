
#install pip install numpy
#pip install openai
#pip install python-dotenv
#pip install azure-core
#pip install azure-cosmos
#pip install tenacity
#pip install --index-url=https://pkgs.dev.azure.com/azure-sdk/public/_packaging/azure-sdk-for-python/pypi/simple/ azure-search-documents==11.4.0a20230509004
import ingest
from dotenv import dotenv_values
from azure.cosmos import CosmosClient,exceptions,PartitionKey
from azure.core.credentials import AzureKeyCredential
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
tex_book = ingest.context('Calculus1','Knowledge Base/demo/Calculus 1_full/Calculus_book_4_2.pdf')
load_data_to_container(tex_book)
print('loaded Calculuc textbook')


tex_book_2 = ingest.context('Calculus1','Knowledge Base/demo/Calculus 1_full/Calculus_book_5.pdf')
load_data_to_container(tex_book_2)
print('loaded second textbook')

tex_book_3 = ingest.context('Calculus1','Knowledge Base/demo/Calculus 1_full/Calculus_book_6.pdf')
load_data_to_container(tex_book_3)
print('loaded third textbook')

tex_book_4 = ingest.context('Calculus1','Knowledge Base/demo/Calculus 1_full/Calculus_book_7.pdf')
load_data_to_container(tex_book_4)
print('loaded fourth textbook')

tex_book_5 = ingest.context('Calculus1','Knowledge Base/demo/Calculus 1_full/Calculus_book_8.pdf')
load_data_to_container(tex_book_5)
print('loaded fifth textbook')

