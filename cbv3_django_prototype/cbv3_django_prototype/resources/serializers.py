from rest_framework import serializers
from .models import Resource
from userauth.serializers import UserSerializer


class TagsSerializerField(serializers.ModelField):

    child = serializers.CharField()
    default_error_messages = {
            'not_a_list': ('Expected a list of tag names but got type "{input_type}".'),
            'not_a_string': ('All list items must be type str.')
                    }

    def __init__(self, **kwargs):
        super(TagsSerializerField, self).__init__(**kwargs)

    def to_internal_value(self, value):
        if not value:
            value = []

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for tag in value:
            if not isinstance(tag, str):
                self.fail('not_a_string')

            self.child.run_validation(tag)

        return value

    def to_representation(self, instance):
        tag_names = instance.tags.names()
        slugs = instance.tags.slugs()

        value = [{'slug': slug, 'name': name} for slug, name in zip(slugs, tag_names)]

        return value


class TagSerializer(serializers.Serializer):

    def create(self, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TagSerializer, self).create(validated_data)

        return self._save_tags(tag_object, to_be_tagged)


    def update(self, instance, validated_data):
        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TagSerializer, self).update(instance, validated_data)

        return self._save_tags(tag_object, to_be_tagged)

    def _save_tags(self, tag_object, tags):
        for key in tags.keys():
            getattr(tag_object, key).set(*tags.get(key))

        return tag_object

    def _pop_tags(self, validated_data):
        to_be_tagged = {key: validated_data.pop(key) for key in self.fields.keys()
                        if isinstance(self.fields[key], TagsSerializerField)
                        and key in validated_data}

        return (to_be_tagged, validated_data)


class ResourceSerializer(TagSerializer, serializers.ModelSerializer):

    tags = TagsSerializerField(model_field='tags')
    media_type = serializers.SerializerMethodField()
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
            'tags',
        )

    def get_media_type(self, obj):
        return obj.get_media_type_display()
