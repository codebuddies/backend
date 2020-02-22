from .models import Resource
from .serializers import ResourceSerializer
from rest_framework import filters, viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated


class ResourceView(viewsets.ModelViewSet, mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)

    queryset = Resource.objects.all()

    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['guid', '^media_type', 'title', 'description']
    lookup_field = 'guid'


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def patch(self, request, guid):
        resource_object = self.get_object(guid)
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
