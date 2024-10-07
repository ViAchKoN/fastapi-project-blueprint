import factory

from core import schemas


class ItemBaseSchemaFactory(factory.Factory):
    class Meta:
        model = schemas.ItemBaseSchema

    name = factory.Faker('word')
    number = factory.Faker('pyint')
    is_valid = factory.Faker('boolean')
