import logging
from fastapi import FastAPI
from azure.identity import (
    DefaultAzureCredential,
)
from azure.keyvault.secrets import SecretClient

app = FastAPI()


@app.get("/")
async def home():
    return "works"


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
