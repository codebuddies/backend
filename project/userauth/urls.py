from django.urls import include, path, re_path, reverse_lazy
from rest_framework import routers
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

app_name = "userauth"
router = routers.SimpleRouter(r'userauth')

urlpatterns = (
    path('', include('dj_rest_auth.urls')),
    path('', include(router.urls)),
    path('registration/', include('dj_rest_auth.registration.urls'), name='registration'),
    path('registration/verify-email/$', views.CustomVerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('registration/verify-email/(?P<key>[-:\w]+)/$', views.CustomVerifyEmailView.as_view(), name='account_confirm_email'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('current_user/', views.current_user),
 )
