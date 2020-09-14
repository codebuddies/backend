from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from dj_rest_auth.serializers import LoginSerializer
from django.conf import settings
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """
    We use get_user_model here because of the custom User model.
    See: https://wsvincent.com/django-referencing-the-user-model/.
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser')
        lookup_field = 'username'

class UserSerializerWithToken(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'token', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

class VerifyEmailSerializer(serializers.ModelSerializer):

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            user = UserSerializer(read_only=True)

            # check if settings swith is on / then check validity
            if settings.ACCOUNT_EMAIL_VERIFICATION == settings.ACCOUNT_EMAIL_VERIFICATION_MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)

                if not email_address.verified:
                    raise serializers.ValidationError(f'Your email is not verified.  Please verify your email before continuing.')

        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)

        return response_data


class UserLoginSerializer(LoginSerializer):

    user = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):

        if settings.ACCOUNT_EMAIL_VERIFICATION == 'mandatory':
            if not EmailAddress.objects.get(email=user.get('email').verified()):
                raise serializers.ValidationError(f'Your email is not verified.  Please verify your email before continuing.')
