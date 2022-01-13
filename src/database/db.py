import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase

from config import settings
from database.models import UserDB

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.database_url, uuidRepresentation="standard"
)
db = client[settings.database_name]
users_collection = db["users"]


def get_user_db():
    yield MongoDBUserDatabase(UserDB, users_collection)
