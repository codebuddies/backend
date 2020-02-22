from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

<<<<<<< HEAD
=======

>>>>>>> d57b07986d5c3e64b97c59609e3bb972d01411aa
class UserSerializer(serializers.ModelSerializer):
    """
    We use get_user_model here because of the custom User model.
    See: https://wsvincent.com/django-referencing-the-user-model/.
    """

    class Meta:
        model = get_user_model()
<<<<<<< HEAD
        fields = ('username', 'is_superuser',)

=======
        fields = ('id', 'username', 'first_name', 'last_name', 'is_superuser',)
        lookup_field = 'username'
>>>>>>> d57b07986d5c3e64b97c59609e3bb972d01411aa

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

<<<<<<< HEAD
=======

>>>>>>> d57b07986d5c3e64b97c59609e3bb972d01411aa
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
<<<<<<< HEAD


=======
>>>>>>> d57b07986d5c3e64b97c59609e3bb972d01411aa
