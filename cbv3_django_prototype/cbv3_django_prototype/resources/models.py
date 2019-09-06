from django.db import models

RESOURCE_TYPE_CHOICES = [
    ("tutorial", "Tutorial"),
    ("course", "Course"),
    ("community", "Community"),
]


class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.CharField(max_length=255, choices=RESOURCE_TYPE_CHOICES)
    credit = models.CharField(max_length=255)
    url = models.URLField()
    referrer = models.CharField(max_length=255)

    def __str__(self):
        return self.title
