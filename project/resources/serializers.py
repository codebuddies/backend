from rest_framework import serializers
from .models import Resource
from userauth.serializers import UserSerializer
from tagging.serializers import TagSerializer, TagsSerializerField


class MediaTypeSerializerField(serializers.ChoiceField):
    def to_representation(self, value):

        valid_media_types = ", ".join(item for item in self.choices)

        if not value:
            return ""

        else:
            try:
                media_type = self.choices[value]

            except KeyError as err:
                raise KeyError(
                    f"Invalid media type.  The media type should be one of the following: {valid_media_types}"
                ) from err

            return media_type

    def to_internal_value(self, value):
        return value


class ResourceSerializer(TagSerializer, serializers.ModelSerializer):

    tags = TagsSerializerField(model_field="tags", default="")
    media_type = MediaTypeSerializerField(
        choices=Resource.RESOURCE_TYPES, allow_blank=True
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Resource
        lookup_field = "guid"

        fields = (
            "guid",
            "author",
            "title",
            "description",
            "url",
            "referring_url",
            "other_referring_source",
            "user",
            "date_published",
            "created",
            "modified",
            "media_type",
            "paid",
            "tags",
        )
