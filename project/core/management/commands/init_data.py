import pprint
import random
from argparse import ArgumentTypeError
from functools import partial

from django.core.management.base import BaseCommand
from factory import PostGenerationMethodCall, create_batch

from users.factories import UserFactory
from users.models import User
from resources.factories import ResourceFactory
from resources.models import Resource
from tagging.factories import CustomTagFactory, TaggedItemsFactory
from tagging.models import CustomTag, TaggedItems


class Command(BaseCommand):

    help = "Initialize the DB with some random fake data for testing and development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear-db",
            action="store_true",
            dest="clear-db",
            help="Clear existing data from the DB before creating test data",
        )

        def check_min_int(min, value):
            ivalue = int(value)
            if ivalue < min:
                raise ArgumentTypeError(f"must be at least {min}")
            return ivalue

        parser.add_argument(
            '--num-users',
            type=partial(check_min_int, 1),
            required=False,
            default=10,
            dest="num-users",
            help="Number of `User` objects to create (default 10)"
        )
        parser.add_argument(
            '--num-tags',
            type=partial(check_min_int, 1),
            required=False,
            default=10,
            dest="num-tags",
            help="Number of `Tag` objects to create (default 10)"
        )
        parser.add_argument(
            '--num-resources',
            type=partial(check_min_int, 2),
            required=False,
            default=10,
            dest="num-resources",
            help="Number of `Resource` objects to create (default 10)"
        )

    def teardown(self):
        TaggedItems.objects.all().delete()
        CustomTag.objects.all().delete()
        Resource.objects.all().delete()
        User.objects.all().delete()

    def create_users(self, num):
        # Create random users.
        # All users have the password 'codebuddies'.
        return create_batch(
            UserFactory,
            num,
            password=PostGenerationMethodCall('set_password', 'codebuddies')
        )

    def create_tags(self, num):
        initial_tag_count = CustomTag.objects.all().count()
        tags = set()
        while CustomTag.objects.all().count() < (initial_tag_count + num):
            tags.add(CustomTagFactory())
        return list(tags)

    def create_resources(self, num):
        return create_batch(ResourceFactory, num, user=random.choice(self.users))

    def tag_resources(self):
        tagged_items = []
        # Assign one resource zero tags, but
        # assign each other resource at least one tag
        for resource in self.resources[:-1]:
            for _ in range(0, random.randrange(1, 4)):
                tag = random.choice(self.tags)
                tagged_items.append(
                    TaggedItemsFactory(content_object=resource, tag=tag),
                )
        return tagged_items

    def print_list(self, lst):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(lst)

    def print_summary(self, verbosity):
        self.stdout.write(f'Created {len(self.users)} Users.')
        if verbosity >= 2:
            self.print_list(self.users)
        self.stdout.write(f'Created {len(self.tags)} Tags.')
        if verbosity >= 2:
            self.print_list(self.tags)
        self.stdout.write(f'Created {len(self.resources)} Resources.')
        if verbosity >= 2:
            self.print_list(self.resources)
        self.stdout.write(f'Created {len(self.tagged_items)} TaggedItems.')
        if verbosity >= 2:
            self.print_list(self.tagged_items)

    def handle(self, *args, **kwargs):
        if kwargs['clear-db']:
            self.stdout.write('Clearing existing data..')
            self.teardown()

        self.stdout.write('Creating test data..')
        self.users = self.create_users(kwargs['num-users'])
        self.tags = self.create_tags(kwargs['num-tags'])
        self.resources = self.create_resources(kwargs['num-resources'])
        self.tagged_items = self.tag_resources()

        self.print_summary(kwargs['verbosity'])

        self.stdout.write('..done')
