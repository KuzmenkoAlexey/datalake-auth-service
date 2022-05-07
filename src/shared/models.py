from pydantic import BaseModel


class UserMixin(BaseModel):
    first_name: str = ""
    last_name: str = ""
