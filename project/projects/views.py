from .models import Project
from .serializers import ProjectSerializer
from rest_framework import filters, viewsets



class ProjectView(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', '^media_type', 'title', 'description', 'tags']

    def patch(self, request, pk):
        project_object = self.get_object(pk)
        serializer_class = ProjectSerializer(project_object, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return JsonResponse(code=201, data=serializer_class.data)
        return JsonResponse(code=400, data="wrong parameters")
'''
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])
'''
