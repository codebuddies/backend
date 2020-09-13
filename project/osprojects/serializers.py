from rest_framework import serializers
from .models import OSProjects
from userauth.serializers import UserSerializer
from tagging.serializers import TagSerializer, TagsSerializerField


class OSProjectsSerializer(TagSerializer, serializers.ModelSerializer):

    tags = TagsSerializerField(model_field="tags", default="")
    user = UserSerializer(read_only=True)

    class Meta:
        model = OSProjects
        lookup_field = "guid"

        fields = (
            "guid",
            "title",
            "project_creator",
            "description",
            "url",
            "user",
            "created",
            "modified",
            "open_to_contributors",
            "tags",
        )
