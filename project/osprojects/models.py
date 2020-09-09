import uuid
from taggit.managers import TaggableManager
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from tagging.managers import CustomTaggableManager
from tagging.models import CustomTag, TaggedItems


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def get_tags_display(self):
    return self.tags.values_list('name', flat=True)


class OSProjects(models.Model):

    guid = models.UUIDField(default=uuid.uuid1, editable=False)

    title = models.CharField(max_length=200)

    project_creator = models.CharField(blank=True, max_length=200)

    description = models.TextField(blank=True, max_length=600)

    # specific URL of project home or github repo
    url = models.URLField(max_length=300)

    # user who posted the project
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))

    # creation date of project entry
    created = models.DateTimeField(auto_now_add=True)

    # modification date of project entry
    modified = models.DateTimeField(default=timezone.now)

    # TO DO:  DEFINE FINAL DATA TYPE OF THIS FIELD
    open_to_contributors = models.BooleanField()

    # TO DO:  DEFINE RELATIONS FOR THIS FIELD
    # contributing_cb_members = ?????

    # Allow tags to be used across entities
    # E.g. so we can create composite views showing all entities sharing a common tag
    tags = TaggableManager(through=TaggedItems, manager=CustomTaggableManager, blank=True)

    def __str__(self):
        """A string representation of the model."""
        return self.title
