import logging
from fastapi import FastAPI
from azure.identity import (
    DefaultAzureCredential,
)
from azure.keyvault.secrets import SecretClient
from storage import service, get_users, add_user

app = FastAPI()


@app.get("/")
async def home():
    key = add_user({"name": "Hänmies", "age": 30, "juu": "joo!"})
    return key


@app.get("/joo")
async def joo():

    users = []
    users_table = service.get_table_client("Users")

    entities = users_table.query_entities(f"PartitionKey eq 'users'")
    for entity in entities:
        user_data = dict(entity)
        users.append(user_data)
    return users


@app.get("/secret")
async def secret():

    try:
        credential = DefaultAzureCredential()
        key_vault_name = "kv-fastapidemo"
        kv_uri = f"https://{key_vault_name}.vault.azure.net"
        client = SecretClient(vault_url=kv_uri, credential=credential)

        secret_name = "testjuttu"
        retrieved_secret = client.get_secret(secret_name)

        return {"secret_name": secret_name, "secret_value": retrieved_secret.value}
    except Exception as e:
        logging.error("Secret fetch failed with: ", e)
        return "failed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
