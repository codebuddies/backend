import uuid
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _



class CustomTag(TagBase):
    guid = models.UUIDField(default=uuid.uuid1, editable=False)
    slug = models.SlugField(
        verbose_name=_("Slug"),
        unique=True,
        max_length=100,
        allow_unicode=True
    )
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)

    class Meta:
        db_table = "tagging_custom_tag"
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        app_label = 'tagging'

    def save(self, *args, **kwargs):
        self.slug = self.slugify(self.name)
        self.full_clean()
        return super().save(*args, **kwargs)

    def slugify(self, tag, i=None):
        return slugify(tag, allow_unicode=True)

class TaggedItems(GenericTaggedItemBase, TaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        unique_together = ("content_type", "object_id", "tag")
