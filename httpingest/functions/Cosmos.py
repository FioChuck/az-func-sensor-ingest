from azure.cosmos import CosmosClient
import os

def create_items(containerval,item):
        client = CosmosClient(os.environ['cosmosEndPoint'], os.environ['cosmosKey'])

        database = client.get_database_client('telemetry')
        container = database.get_container_client(containerval)

        container.create_item(body=item)