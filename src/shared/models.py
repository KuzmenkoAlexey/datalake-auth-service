import typing

from pydantic import BaseModel


class UserMixin(BaseModel):
    first_name: typing.Optional[str] = ""
    last_name: typing.Optional[str] = ""
