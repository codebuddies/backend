import uuid
import regex
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _



class CustomTag(TagBase):
    guid = models.UUIDField(default=uuid.uuid1, editable=False)
    slug = models.SlugField(verbose_name=_("Slug"),  max_length=100, allow_unicode=True)
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)

    class Meta:
        db_table = "tagging_custom_tag"
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        app_label = 'tagging'
        unique_together = ('name', 'slug',)

    def slugify(self, tag, i=None):
        abugidas = regex.compile(
        u"[\p{Bengali}"
        u"\p{Buhid}"
        u"\p{Devanagari}"
        u"\p{Gujarati}"
        u"\p{Gurmukhi}"
        u"\p{Hanunoo}"
        u"\p{Kannada}"
        u"\p{Khmer}"
        u"\p{Lao}"
        u"\p{Limbu}"
        u"\p{Malayalam}"
        u"\p{Mongolian}"
        u"\p{Myanmar}"
        u"\p{Phags-pa}"
        u"\p{Sinhala}"
        u"\p{Tagalog}"
        u"\p{Tamil}"
        u"\p{Telugu}"
        u"\p{Thaana}"
        u"\p{Thai}"
        u"\p{Tibetan}"
        u"\p{Yi}]+", regex.VERBOSE)

        whitespace = regex.compile(u"\p{Z}+")

        if regex.search(abugidas, tag):
            return regex.sub(whitespace, '-', tag.strip().lower())
        else:
            return slugify(tag, allow_unicode=True)


class TaggedItems(GenericTaggedItemBase, TaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
