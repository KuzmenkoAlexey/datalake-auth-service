from fastapi_users import models as user_models

from shared import models as shared_models


class UserDB(shared_models.UserMixin, user_models.BaseUserDB):
    pass
