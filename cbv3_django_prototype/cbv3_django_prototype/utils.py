from userauth.serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None, *args):
    return {
        'token': token,
        'username': UserSerializer(user, context={'request': request}).data['username']
    }
