import uuid
import django.contrib.postgres.fields as pg
from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('VID', 'Video'),
        ('POD', 'Podcast'),
        ('PODEP', 'Podcast Episode'),
        ('TALK', 'Talk'),
        ('TUTOR', 'Tutorial'),
        ('COURSE', 'Course'),
        ('BOOK', 'Book'),
        ('BLOG', 'Blog'),
        ('GAME', 'Game'),
        ('EVENT', 'Event'),
        ('TOOL', 'Tool'),
        ('LIB', 'Library'),
        ('WEB', 'Website')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    title = models.CharField(max_length=200)

    # potentially a markdown field.  Will need a markdown converter and renderer
    description = models.TextField(blank=True, max_length=500)

    # specific URL of resource
    url = models.URLField(max_length=300)

    # the URL of the referring/source site.  e.g. URL of tweet, if it was tweeted.
    referrer = models.URLField(blank=True, max_length=300)

    # names of persons who suggest this resource to the user
    credit = models.CharField(max_length=100)

    # publication date of resource
    date_published = models.DateTimeField(default=timezone.now)

    # creation date of resource entry
    created = models.DateTimeField(auto_now_add=True)

    # modification date of resource entry
    modified = models.DateTimeField(default=timezone.now)

    # [video, podcast, podcast episode, talk, tutorial, course, book, blog, game, event, tool, library]
    media_type = models.CharField(max_length=7, choices=RESOURCE_TYPES)

    paid = models.BooleanField(null=True)

    # Use common storage for tags,
    # so we can create composite views grouping resources and other items by tag
    tags = TaggableManager()

    def __str__(self):
        """A string representation of the model."""
        return self.title
