from rest_framework import serializers
from .models import Resource
from userauth.serializers import UserSerializer
from tagging.serializers import TagSerializer, TagsSerializerField


class MediaTypeSerializerField(serializers.ChoiceField):

    def to_representation(self, value):
            return "" if not value else self.choices[value]

    def to_internal_value(self,  value):
        return value


class ResourceSerializer(TagSerializer, serializers.ModelSerializer):

    tags = TagsSerializerField(model_field='tags', default='')
    media_type = MediaTypeSerializerField(choices=Resource.RESOURCE_TYPES, allow_blank=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Resource
        lookup_field = 'guid'

        fields = (
            'guid',
            'author',
            'title',
            'description',
            'url',
            'referring_url',
            'other_referring_source',
            'user',
            'date_published',
            'created',
            'modified',
            'media_type',
            'paid',
            'tags'
        )
