import uuid
from django.contrib.contenttypes.models import ContentType
from factory import DjangoModelFactory, Faker, LazyAttribute
from .models import CustomTag, TaggedItems


class CustomTagFactory(DjangoModelFactory):
    guid = LazyAttribute(lambda obj: uuid.uuid1())
    name = Faker("word")

    class Meta:
        model = CustomTag
        django_get_or_create = ["guid"]
