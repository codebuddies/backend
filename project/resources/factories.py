import uuid
from random import choice

from factory import DjangoModelFactory, Faker, LazyAttribute, SubFactory

from users.factories import UserFactory
from .models import Resource

RESOURCE_TYPES = [resource[0] for resource in Resource.RESOURCE_TYPES]


class ResourceFactory(DjangoModelFactory):
    guid = LazyAttribute(lambda obj: uuid.uuid1())
    title = Faker("sentence")
    author = Faker("name")
    description = Faker("text")
    url = Faker("uri")
    referring_url = Faker("uri")
    other_referring_source = Faker("uri")
    user = SubFactory(UserFactory)
    media_type = choice(RESOURCE_TYPES)
    paid = choice(["True", "False"])

    class Meta:
        model = Resource
