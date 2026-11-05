import json
import os
import random
from fastapi import FastAPI, HTTPException, Request
import redis.asyncio as redis
from azure.identity import (
    DefaultAzureCredential,
)

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


@app.get("/")
async def home():
    return "works"


@app.get("/api/headers")
async def get_headers(request: Request):
    return {
        "headers": dict(request.headers),
    }


@app.get("/api/redis/write")
async def write_hello():
    try:
        rand_num = random.randint(1, 1000000)
        data = {
            "message": "hello",
            "random_number": rand_num,
        }
        await redis_client.set("hello", json.dumps(data))
        return {"status": "success", "key": "hello", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")


@app.get("/api/redis/read")
async def read_hello():
    try:
        data = await redis_client.get("hello")
        if data is None:
            raise HTTPException(status_code=404, detail="Key 'hello' not found in Redis")
        return {"key": "hello", "data": json.loads(data)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")


@app.get("/api/redis/read-wo-password")
async def read_hello2():
    try:
        redis_client_no_password = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
        )
        data = await redis_client_no_password.get("hello")
        if data is None:
            raise HTTPException(status_code=404, detail="Key 'hello' not found in Redis")
        return {"key": "hello", "data": json.loads(data)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
