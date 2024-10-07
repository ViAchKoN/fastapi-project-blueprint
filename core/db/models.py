import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

import typing


class BaseModel(DeclarativeBase):
    def as_dict(self) -> typing.Dict[str, str]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore


class Item(BaseModel):
    __tablename__ = "item"

    id_seq = sa.Sequence("seq_item_id", metadata=BaseModel.metadata)

    id = mapped_column(sa.Integer, primary_key=True, server_default=id_seq.next_value(),)
    name: Mapped[str]
    number: Mapped[typing.Optional[int]]
    is_valid: Mapped[bool] = mapped_column(default=False, server_default='false', nullable=False)
