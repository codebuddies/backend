from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectView, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    path('project/', include('rest_framework.urls', namespace='rest_framework')),
]
