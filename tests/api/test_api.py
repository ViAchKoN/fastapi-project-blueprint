import json
from unittest.mock import ANY

from fastapi import status

from core.db.models import Item
from tests import factories


def test_get_items(fastapi_test_client):
    expected_items = factories.models_factory.ItemModelFactory.create_batch(size=5)

    response = fastapi_test_client.get(
        "/items",
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data == [
        {
            "id": item.id,
            "name": item.name,
            "number": item.number,
            "is_valid": item.is_valid,
        }
        for item in expected_items
    ]


def test_post_items(
    fastapi_test_client,
    test_db_session,
):
    assert test_db_session.query(Item).first() is None

    item_to_add = factories.schemas_factory.ItemBaseSchemaFactory.create()

    response = fastapi_test_client.post(
        "/items",
        data=json.dumps(
            {
                "items": [item_to_add.dict()],
            },
            default=str,
        ),
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data == [
        {
            "id": ANY,
            "name": item_to_add.name,
            "number": item_to_add.number,
            "is_valid": item_to_add.is_valid,
        },
    ]

    assert (
        test_db_session.query(Item)
        .filter(
            Item.name == item_to_add.name,
            Item.number == item_to_add.number,
            Item.is_valid == item_to_add.is_valid,
        )
        .first()
    )


def test_update_item(
    fastapi_test_client,
    test_db_session,
):
    item = factories.models_factory.ItemModelFactory.create()

    update_data = factories.schemas_factory.ItemBaseSchemaFactory.create()

    response = fastapi_test_client.patch(
        f"/items/{item.id}",
        data=json.dumps(
            {
                "update_data": update_data.dict(),
            },
            default=str,
        ),
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data == {
        "id": ANY,
        "name": update_data.name,
        "number": update_data.number,
        "is_valid": update_data.is_valid,
    }

    assert (
        test_db_session.query(Item)
        .filter(
            Item.name == update_data.name,
            Item.number == update_data.number,
            Item.is_valid == update_data.is_valid,
        )
        .first()
    )


def test_delete_item(
    fastapi_test_client,
    test_db_session,
):
    item = factories.models_factory.ItemModelFactory.create()

    response = fastapi_test_client.delete(
        f"/items/{item.id}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert test_db_session.query(Item).first() is None
