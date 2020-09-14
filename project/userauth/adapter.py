from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        url = settings.CUSTOM_ACCOUNT_CONFIRM_EMAIL_URL.format(emailconfirmation.key)
        result = build_absolute_uri(request, url)
        return result
