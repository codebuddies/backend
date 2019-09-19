from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            'id',
            'title',
            'description',
            'url',
            'referrer',
            'credit',
            'date_published',
            'created',
            'modified',
            'type',
            'paid',
            'tags',
        )
