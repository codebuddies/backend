from rest_framework import serializers

from .models import Resource


class ResourceSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("title", "description", "resource_type", "credit", "url", "referrer")
