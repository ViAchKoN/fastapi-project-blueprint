from fastapi import FastAPI, Body, HTTPException

from core.db import queries
from core import schemas

app = FastAPI()


@app.get(
    "/",
    summary="Health Check",
    status_code=200,
)
async def health_check() -> dict:
    return {"status": "ok"}


@app.get(
    "/items",
    summary="Get items",
    status_code=200,
    response_model=list[schemas.ItemSchema],
)
def get_items() -> list[schemas.ItemSchema]:
    items = queries.get_items()
    return items


@app.post(
    "/items",
    summary="Add items",
    status_code=200,
    response_model=list[schemas.ItemSchema],
)
def add_items(
    items: list[schemas.ItemBaseSchema] = Body(
        ...,
        embed=True,
    )
) -> list[schemas.ItemSchema]:
    added_items = queries.add_items(
        items=items
    )
    return added_items


@app.patch(
    "/items/{item_id}",
    summary="Update an item",
    status_code=200,
    response_model=schemas.ItemSchema,
)
def update_item(
    item_id: int,
    update_data: schemas.ItemBaseSchema = Body(
        ...,
        embed=True,
    )
) -> None:
    if queries.get_item(
        item_id=item_id
    ) is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item = queries.update_item(
        item_id=item_id,
        update_data=update_data,
    )
    return item


@app.delete(
    "/items/{item_id}",
    summary="Delete an item",
    status_code=204,
)
def delete_item(
    item_id: int
) -> None:
    if queries.get_item(
        item_id=item_id
    ) is None:
        raise HTTPException(status_code=404, detail="Item not found")

    queries.delete_item(
        item_id=item_id
    )
