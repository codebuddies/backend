import uuid
from django.contrib.contenttypes.models import ContentType
from factory import (
    DjangoModelFactory,
    Faker,
    LazyAttribute,
    SubFactory,
    SelfAttribute
)

from resources.factories import ResourceFactory
from .models import CustomTag, TaggedItems


class CustomTagFactory(DjangoModelFactory):
    guid = LazyAttribute(lambda obj: uuid.uuid1())
    name = Faker("word")

    class Meta:
        model = CustomTag
        django_get_or_create = ["name"]


class TaggedItemsFactory(DjangoModelFactory):

    content_type = LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))
    content_object = SubFactory(ResourceFactory)
    object_id = SelfAttribute('content_object.id')
    tag = SubFactory(CustomTagFactory)

    class Meta:
        model = TaggedItems
        django_get_or_create = ["content_type", "object_id", "tag"]
