from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
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
    path('', include(router.urls)),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('registration/verify-email/', views.VerifyEmailView.as_view(), name='email_confirm'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view()),
 )

#EmailAddress.objects.filter(user=self.request.user, verified=True).exists()

#(?P<key>[-:\w]+)/$'
