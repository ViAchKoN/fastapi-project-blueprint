import typing

from pydantic import BaseModel


class ItemBaseSchema(BaseModel):
    name: str
    number: typing.Optional[int]
    is_valid: typing.Optional[bool]


class ItemSchema(ItemBaseSchema):
    id: int
    is_valid: bool
