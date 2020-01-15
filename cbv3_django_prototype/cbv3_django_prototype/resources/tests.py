from rest_framework import status, serializers
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from django.core.management import call_command
from django.contrib.auth import get_user_model

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ResourcesTests(APITestCase):

    def setUp(self):
        """
        Loads users.json and resources.json fixtures into test DB
        """
        call_command('loaddata', 'users.json', verbosity=0)
        call_command('loaddata', 'resources.json', verbosity=0)
        model = get_user_model()
        self.person = model.objects.create_user(username='PetuniaPig', email='pretty.piglet@pigfarm.org',
                                           password='codebuddies', is_superuser=True)

        url = '/auth/obtain_token/'
        data = {"username": "PetuniaPig", "password": "codebuddies"}
        token_response = self.client.post(url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])


    def test_view_resources(self):
        url = '/api/v1/resources/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_search_resources(self):
        url = '/api/v1/resources/?search=Elm'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertContains(response, "Elm Crash-Course (Reactivate London)")


    def test_view_one_resource(self):
        url = '/api/v1/resources/f7f8ee30-da8e-11e9-8a1f-d20089b01401/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "PyCon Israel, Tel Aviv Keynote:  The Fun of Reinvention - David Beazly")


    def test_patch_one_resource(self):
        url = '/api/v1/resources/f7f8ee30-da8e-11e9-8a1f-d20089b01401/'
        data= {
            "description": "A _diabolically irresponsible_ talk in which I celebrate modern Python coding by **abandoning all backwards compatibility** THE END"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])


    def test_delete_one_resource(self):
        url = '/api/v1/resources/f7f8ee30-da8e-11e9-8a1f-d20089b01401/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        subsequent_response = self.client.get(url)
        self.assertEqual(subsequent_response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_one_resource(self):
        url = '/api/v1/resources/'
        data = {"title": "The Modern JavaScript Tutorial",
             "author":"iliakan",
             "description":"How it's done now. From the basics to advanced topics with simple, but detailed explanations. Main course contains 2 parts which cover JavaScript as a programming language and working with a browser. There are also additional series of thematic articles.",
             "url":"https://javascript.info/",
             "referring_url":"https://gitconnected.com/learn/javascript",
             "other_referring_source": "iliakan@javascript.info",
             "user":15,
             "date_published":"2019-09-19T03:27:06Z",
             "created":"2019-09-19T03:27:06.485Z",
             "modified":"2019-09-19T03:27:06Z",
             "media_type":"WEB",
             "tags":[
                    {
                       "id":"a1167632-abb8-4ce1-b090-b84e79c94c7f",
                       "name":"JavaScript"
                    },
                    {
                       "id":"0d325a30-7262-4914-90fe-6c90ac725fc2",
                       "name":"FrontEnd"
                    }
                    ]
             }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "The Modern JavaScript Tutorial")
        self.assertEqual(response.data['other_referring_source'], "iliakan@javascript.info")

