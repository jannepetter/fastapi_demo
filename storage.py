import os
from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv("ENV", "DEV")


def create_service():
    if ENV == "DEV":
        connection_string = (
            "DefaultEndpointsProtocol=http;"
            "AccountName=devstoreaccount1;"
            "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"  # default azurite accountkey
            "TableEndpoint=http://azurite:10002/devstoreaccount1;"
        )
        service = TableServiceClient.from_connection_string(conn_str=connection_string)
        return service

    credential = DefaultAzureCredential()
    storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")

    service = TableServiceClient(
        endpoint=f"https://{storage_account_name}.table.core.windows.net/",
        credential=credential,
    )

    return service


def init_storage_tables(service: TableServiceClient):
    service.create_table_if_not_exists("Users")
    service.create_table_if_not_exists("Orders")


def init_stuff():
    service = create_service()
    init_storage_tables(service)

    return service


service = init_stuff()


def add_user(user_dict, partition_key="users"):
    row_key = datetime.now().strftime("%Y%m%d%H%M%S%f") + "_" + str(uuid.uuid4())[:8]
    users_table = service.get_table_client("Users")
    # Prepare entity
    entity = {
        "PartitionKey": partition_key,
        "RowKey": row_key,
        **user_dict,  # Add all user properties
    }

    # Insert entity
    users_table.create_entity(entity)

    return row_key


def get_users(partition_key="users"):

    users = []
    users_table = service.get_table_client("Users")

    entities = users_table.query_entities(f"PartitionKey eq '{partition_key}'")
    for entity in entities:

        user_data = dict(entity)
        user_data["timestamp"] = entity.metadata["timestamp"]
        users.append(user_data)
    return users
