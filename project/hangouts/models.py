import uuid
import datetime
from taggit.managers import TaggableManager
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from resources.models import Resource
from tagging.managers import CustomTaggableManager
from tagging.models import CustomTag, TaggedItems


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def get_tags_display(self):
    return self.tags.values_list('name', flat=True)


class Hangout(models.Model):
    HANGOUT_TYPES = [
        ('WATCH', 'Watch Me Code'),
        ('PRES', 'Presentation'),
        ('COWRK', 'Co-work with Me'),
        ('STUDY', 'Study Group'),
        ('PAIR', 'Pairing'),
        ('ACNT', 'Keep Me Accountable'),
        ('DISC', 'Discussion'),
        ('TEACH', 'I have something to teach'),
    ]

    guid = models.UUIDField(default=uuid.uuid1, editable=False)

    #One of scheduled, pending, rescheduled, stale, hold, closed, completed
    status = models.CharField(blank=True, max_length=200)
    hangout_type = models.CharField(max_length=6, choices=HANGOUT_TYPES)

    #we are going to require a title
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(verbose_name=_("Slug"),  max_length=100, allow_unicode=True)
    short_description = models.TextField(max_length=300, blank=False, null=False)
    long_description = models.TextField(max_length=600, blank=True, null=True)

    # user who "owns" the hangout we'll pull this from their TOKEN
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))

    #sort of a public/private thing and confirmed/not confirmed thing
    open_to_RSVP = models.BooleanField(blank=False, null=False, default=False)

    #Calendar date + start time would be derived from the datetime object
    start_time = models.DateTimeField(default=timezone.now)

    #Calendar date + end time would be derived from the datetime object
    end_time = models.DateTimeField(blank=False, null=False)

    # creation date of hangout entry
    created = models.DateTimeField(auto_now_add=True)

    # modification date of hangout entry
    modified = models.DateTimeField(default=timezone.now)

    recurring = models.BooleanField(null=False, default=False)

    internal_platform = models.BooleanField(null=False, default=True)
    external_platform_link = models.URLField(max_length=300, blank=True, null=True)

    related_resources = models.ManyToManyField(Resource, blank=True, related_name='related_hangouts')

    # Allow tags to be used across entities
    # E.g. so we can create composite views showing all entities sharing a common tag
    tags = TaggableManager(through=TaggedItems, manager=CustomTaggableManager, blank=True)


class HangoutSessions(models.Model):
    guid = models.UUIDField(default=uuid.uuid1, editable=False)
    hangout_id = models.ForeignKey(Hangout, on_delete=models.CASCADE, blank=True, null=True, related_name='related_sessions')
    status = models.CharField(blank=True, max_length=200) #scheduled, pending, rescheduled, stale, hold, closed, completed
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=False, null=False)
    related_resources = models.ManyToManyField(Resource, blank=True, related_name='related_hangout_sessions')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=timezone.now)


class HangoutResponses(models.Model):
    guid = models.UUIDField(default=uuid.uuid1, editable=False)
    hangout_id = models.ForeignKey(Hangout, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='related_responses')
    hangout_session_id = models.ForeignKey(HangoutSessions, on_delete=models.CASCADE, blank=True, null=True,
                                           related_name='related_session_responses')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    express_interest = models.BooleanField(blank=False, null=False, default=False)
    request_to_join = models.BooleanField(blank=False, null=False, default=False)
    rsvp = models.BooleanField(blank=False, null=False, default=False)
    response_comment = models.TextField(max_length=300, blank=True, null=True)
    status = models.TextField(max_length=10, blank=False, null=False)

