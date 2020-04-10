from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    media_type = serializers.SerializerMethodField()

    class Meta:
        model = Project

        fields = (
            'id',
            'title',
            'maintainer',
            'description',
            'url',
            'user',
            'date_published',
            'created',
            'modified',
            'media_type',
            'open_to_contributors',
            'tags',
            'contributors',
        )

    def get_media_type(self, obj):
        return obj.get_media_type_display()
