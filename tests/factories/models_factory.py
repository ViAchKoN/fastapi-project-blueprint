import factory

from core.db import models
from tests import conftest


class CustomSQLAlchemyModelFactory(factory.Factory):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        with conftest.db_test_session() as session:
            session.expire_on_commit = False
            obj = model_class(*args, **kwargs)
            session.add(obj)
            session.commit()
            session.expunge_all()
        return obj


class ItemModelFactory(CustomSQLAlchemyModelFactory):
    class Meta:
        model = models.Item

    name = factory.Faker("word")
    number = factory.Faker("pyint")
    is_valid = factory.Faker("boolean")
