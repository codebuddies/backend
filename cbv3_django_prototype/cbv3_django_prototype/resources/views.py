from .models import Resource
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.fields import JSONField
from .serializers import ResourceSerializer
from rest_framework import filters, viewsets
from rest_framework.response import Response


class ResourceListView(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', '']
