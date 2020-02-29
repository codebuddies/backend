import uuid
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _



class CustomTag(TagBase):
    guid = models.UUIDField(default=uuid.uuid1, editable=False)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100)
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)

    class Meta:
        db_table = "tagging_custom_tag"
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        app_label = 'tagging'


    def slugify(self, tag, i=None):
        slug = slugify(tag, allow_unicode=True)

        if i is not None:
            slug += "_%d" % i

        return slug


class TaggedItems(GenericTaggedItemBase, TaggedItemBase):
    tag = models.ForeignKey(CustomTag,
                            on_delete=models.CASCADE,
                            related_name="%(app_label)s_%(class)s_items",
                            )

    class Meta:
        db_table = "tagging_tagged_item"
        app_label = "taggit"
