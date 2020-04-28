from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from core.management.commands.init_data import Command
from users.models import User
from resources.models import Resource
from tagging.models import CustomTag, TaggedItems


class InitDataTest(TestCase):

    def test_defaults(self):
        out = StringIO()
        call_command("init_data", stdout=out)
        log = out.getvalue()

        self.assertEqual(10, User.objects.all().count())
        self.assertIn('Created 10 Users.', log)

        self.assertEqual(10, CustomTag.objects.all().count())
        self.assertIn('Created 10 Tags.', log)

        self.assertEqual(10, Resource.objects.all().count())
        self.assertIn('Created 10 Resources.', log)

        # The number of TaggedItems we will insert is non-deterministic,
        # but the lower bound is 9
        self.assertGreaterEqual(TaggedItems.objects.all().count(), 9)

    def test_params(self):
        out = StringIO()
        call_command("init_data", stdout=out, **{
            'num-users': 24,
            'num-tags': 26,
            'num-resources': 28,
        })
        log = out.getvalue()

        self.assertEqual(24, User.objects.all().count())
        self.assertIn('Created 24 Users.', log)

        self.assertEqual(26, CustomTag.objects.all().count())
        self.assertIn('Created 26 Tags.', log)

        self.assertEqual(28, Resource.objects.all().count())
        self.assertIn('Created 28 Resources.', log)

        self.assertGreaterEqual(TaggedItems.objects.all().count(), 27)

    def test_clear_db(self):
        out = StringIO()
        # set up some non-zero amount of data and assert it is there
        call_command("init_data", stdout=out)
        self.assertGreaterEqual(User.objects.all().count(), 1)
        self.assertGreaterEqual(CustomTag.objects.all().count(), 1)
        self.assertGreaterEqual(Resource.objects.all().count(), 1)
        self.assertGreaterEqual(TaggedItems.objects.all().count(), 1)

        cmd = Command()
        # clear it
        cmd.teardown()

        # check its all gone
        self.assertEqual(0, User.objects.all().count())
        self.assertEqual(0, CustomTag.objects.all().count())
        self.assertEqual(0, Resource.objects.all().count())
        self.assertEqual(0, TaggedItems.objects.all().count())
