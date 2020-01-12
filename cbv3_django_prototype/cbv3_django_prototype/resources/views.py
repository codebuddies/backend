from .models import Resource
from .serializers import ResourceSerializer
from rest_framework import filters, viewsets
from rest_framework import mixins

class ResourceView(viewsets.ModelViewSet):

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', '^media_type', 'title', 'description', 'tags']

    def patch(self, request, pk):
        resource_object = self.get_object(pk)
        serializer_class = ResourceSerializer(resource_object, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return JsonResponse(code=201, data=serializer_class.data)
        return JsonResponse(code=400, data="wrong parameters")


'''
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])
'''
