from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.models import Site
from allauth.utils import build_absolute_uri
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        url = settings.CUSTOM_ACCOUNT_CONFIRM_EMAIL_URL.format(emailconfirmation.key)
        result = build_absolute_uri(request, url)
        return result

    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        email_address.verified = True
        email_address.set_as_primary(conditional=True)
        email_address.save()
