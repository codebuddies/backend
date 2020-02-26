from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .views import current_user, UserList

app_name = "userauth"

urlpatterns = [
    path('obtain_token/', obtain_jwt_token),
    path('refresh_token/', refresh_jwt_token),
    path('validate_token/', verify_jwt_token),
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
]
