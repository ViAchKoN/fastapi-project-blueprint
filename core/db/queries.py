from sqlalchemy import create_engine, select, delete, update
from sqlalchemy.orm import sessionmaker

from core.db.models import Item
from core import settings, schemas

sync_engine = create_engine(settings.DB_URL)
sync_session = sessionmaker(autoflush=False, bind=sync_engine)


def get_item(item_id: int):
    with sync_session() as session:
        item = session.execute(
            select(Item).filter(Item.id == item_id)
        ).scalar()
    return item.as_dict() if item else None


def get_items():
    with sync_session() as session:
        items = session.execute(
            select(Item)
        ).scalars().all()
    return [item.as_dict() for item in items]


def update_item(
    item_id: int,
    update_data: schemas.ItemBaseSchema,
):
    with sync_session() as session:
        session.execute(
            update(Item).filter(Item.id == item_id).values(
                **update_data.dict()
            )
        )
        session.commit()
    return get_item(item_id=item_id)


def delete_item(item_id: int):
    with sync_session() as session:
        session.execute(
            delete(Item).filter(Item.id == item_id)
        )
        session.commit()


def add_items(
    items: list[schemas.ItemBaseSchema],
):
    to_add = []
    for item in items:
        to_add.append(
            Item(**item.dict(exclude_none=True))
        )
    with sync_session() as session:
        session.add_all(to_add)
        session.commit()

        for item in to_add:
            session.refresh(item)

    return [item.as_dict() for item in to_add]
