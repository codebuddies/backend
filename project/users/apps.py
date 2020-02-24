from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "cbv3_django_prototype.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import cbv3_django_prototype.users.signals  # noqa F401
        except ImportError:
            pass
