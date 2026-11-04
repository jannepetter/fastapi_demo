from fastapi import FastAPI, Request
from azure.identity import (
    DefaultAzureCredential,
)

app = FastAPI()


@app.get("/")
async def home():
    return "works"


@app.get("/api/aad-tokens")
async def get_aad_tokens(request: Request):
    return {
        "x-ms-token-aad-access-token": request.headers.get("x-ms-token-aad-access-token"),
        "x-ms-token-aad-id-token": request.headers.get("x-ms-token-aad-id-token"),
        "x-ms-client-principal": request.headers.get("x-ms-client-principal"),
        "x-ms-client-principal-name": request.headers.get("x-ms-client-principal-name"),
    }

# @app.post("/api/redis/{key}")
# async def store_data(key: str, request: Request):
#     data = await request.json()

#     await redis_client.set(key, json.dumps(data))

#     return {"key": key, "stored": True}


# @app.get("/api/redis/{key}")
# async def get_data(key: str):
#     data = await redis_client.get(key)

#     if data is None:
#         raise HTTPException(404, "Key not found")

#     return {
#         "key": key,
#         "data": json.loads(data)
#     }