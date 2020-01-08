from rest_framework import serializers
from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    media_type = serializers.SerializerMethodField()

    class Meta:
        model = Resource

        fields = (
            'id',
            'author',
            'title',
            'description',
            'url',
            'referrer',
            'credit',
            'date_published',
            'created',
            'modified',
            'media_type',
            'paid',
            'tags',
        )

    def get_media_type(self, obj):
        return obj.get_media_type_display()
