from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework import routers, serializers, viewsets
from resources.urls import router as resources_router
from userauth.urls import router as userauth_router

router = routers.DefaultRouter()
router.registry.extend(resources_router.registry)
router.registry.extend(userauth_router.registry)

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # User management
    #currently an unused endpoint, but can be used if needed for extended user profiles, etc.
    path("users/", include("users.urls", namespace="users")),

    #we have to include these for registration email validation, but otherwise these paths are NOT used
    path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here
    #this is a route for logging into the "browsable api"  if not needed for testing, it should be omitted.
    path('api/v1/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/auth/', include(('userauth.urls', 'userauth'), namespace="userauth")),
    path('api/v1/', include('resources.urls', namespace='resources')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error
             ),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
