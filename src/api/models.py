from fastapi_users import models as user_models

from shared import models as shared_models


class User(shared_models.UserMixin, user_models.BaseUser):
    pass


class UserCreate(shared_models.UserMixin, user_models.BaseUserCreate):
    pass


class UserUpdate(shared_models.UserMixin, user_models.BaseUserUpdate):
    pass
