from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'resources'
router = routers.SimpleRouter()
router.register(r'resources', views.ResourceView, basename='resources')

urlpatterns = [
    path('', include(router.urls)),
]
