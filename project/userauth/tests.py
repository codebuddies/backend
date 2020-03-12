from unittest.mock import patch
from rest_framework import status, serializers
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserauthTests(APITestCase):

    fixtures = ['users']

    def setUp(self):
        # create a new user
        model = get_user_model()
        self.person = model.objects.create_user(
            username='PetuniaPig',
            email='pretty.piglet@pigfarm.org',
            password='codebuddies'
        )


    def test_jwt_not_authed(self):
        """
        Ensure that if we aren't authed with a token, we don't get to view the
        current_user
        """

        url = '/auth/current_user/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_jwt_auth(self):
        """
        Ensure we can obtain a token with a valid UN and PW combo.
        """

        url = '/auth/obtain_token/'
        data = {"username": "JuJu", "password": "codebuddies"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')


    def test_jwt_validate(self):
        """
        Ensure we can validate a previously acquired token.
        """

        token_response = self.client.post('/auth/obtain_token/', {"username": "PetuniaPig", "password": "codebuddies"}, format='json')
        token = token_response.data['token']
        url = '/auth/validate_token/'
        data = {"token": token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, token)
        self.assertContains(response, 'PetuniaPig')


    def test_jwt_current_user(self):
        """
        Ensure that if we obtain a token in the 'browser',
        we can retrieve the current_user based on the browser token
        """

        token_response = self.client.post('/auth/obtain_token/', {"username": "Phillippp", "password": "codebuddies"},
                                          format='json')
        url = '/auth/current_user/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Phillippp')
        self.assertContains(response, 'is_superuser')


    def test_jwt_refresh(self):
        """
        Ensure that if we ask for a token refresh based on our current token
        we get a refreshed token in return.
        """

        token_response = self.client.post('/auth/obtain_token/', {"username": "Rossie_Rickardsson", "password": "codebuddies"},
                                          format='json')
        url = '/auth/refresh_token/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])
        data = {"token": token_response.data['token']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token_response.data['token'], response.data['token'], msg=None)


    @patch('rest_framework_jwt.serializers.RefreshAuthTokenSerializer.validate')
    def test_jwt_expired_refresh(self, validate_mock):
        """
        Ensure that a request to refresh and expired token fails.
        """
        token_response = self.client.post('/auth/obtain_token/',
                                          {"username": "HenryMelan", "password": "codebuddies"},
                                          format='json')
        url = '/auth/refresh_token/'
        data = {"token": token_response.data['token']}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])
        validate_mock.side_effect = serializers.ValidationError('Refresh has expired.')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    @patch('rest_framework_jwt.serializers._check_payload')
    def test_jwt_expired_token_validate(self, validate_mock):
        """
        Ensure that a request to validate an expired token fails.
        """
        token_response = self.client.post('/auth/obtain_token/',
                                          {"username": "Milty", "password": "codebuddies"},
                                          format='json')

        url = '/auth/validate_token/'
        data = {"token": token_response.data['token']}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])
        validate_mock.side_effect = serializers.ValidationError('Token has expired.')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    @patch('rest_framework_jwt.serializers._check_payload')
    def test_jwt_expired_token_access(self, validate_mock):
        """
        Ensure that a request to a protected api endpoint fails with an
        expired token.
        """
        token_response = self.client.post('/auth/obtain_token/',
                                          {"username": "FWormell", "password": "codebuddies"},
                                          format='json')

        url = '/api/v1/resources/'
        data = {"token": token_response.data['token']}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])
        validate_mock.side_effect = serializers.ValidationError('Token has expired.')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_new_user(self):
        """
        Ensure that a new user is created in the DB and a token for that user
        is returned with valid confirmation data.
        """

        url = '/auth/users/'
        data = {
                "username": "claudette",
                "password": "codebuddies",
                "first_name": "Cali",
                "last_name": "French",
                "email": "asificare@mailme.net"
                }
        token_response = self.client.post('/auth/obtain_token/',
                                          {"username": "Andi3", "password": "codebuddies"},
                                          format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'claudette')
        self.assertEqual((response.data['first_name'], response.data['last_name']),('Cali', 'French'))
        self.assertEqual(response.data['email'], 'asificare@mailme.net')
        self.assertContains(response, 'token', status_code=201)

