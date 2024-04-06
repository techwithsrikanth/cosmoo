from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

async def connect_to_mongo():
    client = AsyncIOMotorClient(MONGO_URL)
    return client

async def close_mongo_connection(client):
    client.close()
