import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase

from config import settings
from database.models import UserDB


class DatabaseWrapper:
    __client = None
    __db = None
    __users_collection = None
    __loop = None

    @classmethod
    def set_event_loop(cls, loop):
        cls.__loop = loop

    @classmethod
    def get_client(cls):
        if cls.__client is None:
            kwargs = {"uuidRepresentation": "standard"}
            if cls.__loop:
                kwargs["io_loop"] = cls.__loop
            cls.__client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.database_url, **kwargs
            )
        return cls.__client

    @classmethod
    def get_db(cls):
        if cls.__db is None:
            client = cls.get_client()
            cls.__db = client[settings.database_name]
        return cls.__db

    @classmethod
    def get_users_collection(cls):
        if cls.__users_collection is None:
            db = cls.get_db()
            cls.__users_collection = db["users"]
        return cls.__users_collection


def get_user_db():
    yield MongoDBUserDatabase(UserDB, DatabaseWrapper.get_users_collection())
