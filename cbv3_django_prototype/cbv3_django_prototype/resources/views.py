from .models import Resource
from .serializers import ResourceSerializer
from rest_framework import filters, viewsets


class ResourceView(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'media_type', 'title', 'description', 'tags']
