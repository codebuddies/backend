import uuid
from random import choice
from factory import DjangoModelFactory, Faker, fuzzy, LazyAttribute, SubFactory
import datetime
from users.factories import UserFactory
from .models import OSProjects


class OSProjectsFactory(DjangoModelFactory):
    """
        Define OSProjects Factory
    """
    guid = LazyAttribute(lambda obj: uuid.uuid1())
    title = Faker("sentence")
    project_creator = Faker("name")
    description = Faker("text")
    url = Faker("uri")
    user = SubFactory(UserFactory)
    created = fuzzy.FuzzyDate(datetime.date(2019, 1, 1))
    modified = fuzzy.FuzzyDate(datetime.date(2020, 1, 1))
    open_to_contributors = choice(["True", "False"])
    tags = fuzzy.FuzzyChoice(['javascript', 'python', 'react', 'go'])

    class Meta:
        model = OSProjects
