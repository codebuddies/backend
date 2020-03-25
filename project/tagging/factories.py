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


"""
TODO:
I've not tested this because we need a ResourceFactory first but based on the
https://factoryboy.readthedocs.io/en/latest/recipes.html#django-models-with-genericforeignkeys
our TaggedItemsFactory is probably going to look roughly like this:

from resources.factories import ResourceFactory

class TaggedItemsFactory(DjangoModelFactory):

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))
    content_object = factory.SubFactory(ResourceFactory)
    object_id = factory.SelfAttribute('content_object.id')
    tag = factory.SubFactory(CustomTagFactory)

    class Meta:
        model = TaggedItems
"""
