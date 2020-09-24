from rest_framework import serializers
from dj_rest_auth.serializers import JWTSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from dj_rest_auth.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model


#customize this for a user profile view
class UserSerializer(serializers.ModelSerializer):
    """
    We use get_user_model here because of the custom User model.
    See: https://wsvincent.com/django-referencing-the-user-model/.
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'is_superuser',)
        lookup_field = 'username'


#customize this for a user profile change
class CustomUserDetailSerializer(UserDetailsSerializer):
    """
    We use get_user_model here because of the custom User model.
    See: https://wsvincent.com/django-referencing-the-user-model/.
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser')
        lookup_field = 'username'


#customize this for a user email validation link
class CustomVerifyEmailSerializer(VerifyEmailSerializer):
    key = serializers.CharField()


#customize this for the password reset email.
class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}


#customize this for the passowrd reset confirmation
class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    pass
