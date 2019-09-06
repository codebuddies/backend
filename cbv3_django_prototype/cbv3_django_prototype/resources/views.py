from rest_framework import viewsets
from .serializers import ResourceSerialiazer
from .models import Resource


class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Resources to be viewed or edited.
    """

    queryset = Resource.objects.all()
    serializer_class = ResourceSerialiazer
