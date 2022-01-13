from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase

from api.models import User, UserCreate, UserUpdate
from config import settings
from database.db import get_user_db
from database.models import UserDB
from utils.logger import setup_logger

LOGGER = setup_logger()


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = settings.jwt_secret
    verification_token_secret = settings.jwt_secret

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        LOGGER.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        LOGGER.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        LOGGER.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


def get_user_manager(user_db: MongoDBUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


jwt_authentication = JWTAuthentication(
    secret=settings.jwt_secret,
    lifetime_seconds=settings.jwt_lifetime_seconds,
    tokenUrl="auth/jwt/login",
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
