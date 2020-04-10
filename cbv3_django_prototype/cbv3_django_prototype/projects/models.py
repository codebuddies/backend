import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
import django.contrib.postgres.fields as pg
from django.contrib.auth import get_user_model
from django.apps import apps


# WHAT NEEDS TO BE DONE:
    # FIX PROJECT_TYPES (Lines 18-31 and Line 65)
    # ADD NEWS MODEL FIELD VALUES FROM PROJECT.JSON FILE


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

from taggit.managers import TaggableManager


class Project(models.Model):
    # dynamically load resources model
    Resources = apps.get_model('resources', 'Resources')

    # create many to many relationship
    resources = models.ManyToManyField(Resources)

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    title = models.CharField(max_length=200)
    
    maintainer = models.CharField(max_length=200, blank=True)

    # potentially a markdown field.  Will need a markdown converter and renderer
    description = models.TextField(blank=True, max_length=300)

    # specific URL of resource
    url = models.URLField(max_length=300)

    # the URL of the referring/source site.  e.g. URL of tweet, if it was tweeted.
    referring_url = models.URLField(blank=True, max_length=300)

    # place or person the user received the recommendation from if not a URL
    other_referring_source = models.CharField(max_length=200)

    # user who posted the resource
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))

    # publication date of resource
    date_published = models.DateTimeField(default=timezone.now)

    # creation date of resource entry
    created = models.DateTimeField(auto_now_add=True)

    # modification date of resource entry
    modified = models.DateTimeField(default=timezone.now)

    open_to_contributors = models.BooleanField(null=True)

    # JSONB for a simplified DB Schema and prototype for now.
    #tags = pg.JSONField()
    # Allow tags to be used across entities
    # E.g. so we can create composite views showing all entities sharing a common tag
    tags = TaggableManager(blank=True)

    def __str__(self):
        """A string representation of the model."""
        return self.title
