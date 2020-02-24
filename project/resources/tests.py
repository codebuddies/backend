from rest_framework import status, serializers
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from django.core.management import call_command

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ResourcesTests(APITestCase):

    def setUp(self):

        call_command('loaddata', 'users.json', verbosity=0)
        call_command('loaddata', 'resources.json', verbosity=0)
        call_command('loaddata', 'tags.json', verbosity=0)

        url = '/auth/obtain_token/'
        #to do:  choose a user at random from loaded users.json
        data = {"username": "JuJu", "password": "codebuddies"}
        token_response = self.client.post(url, data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])


    def test_view_resources(self):
        url = '/api/v1/resources/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 31)


    def test_search_resources(self):
        url = '/api/v1/resources/?search=Elm'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertContains(response, "Elm Crash-Course (Reactivate London)")


    def test_view_one_resource(self):
        url = '/api/v1/resources/?search=Katie Hughes'
        guid = self.client.get(url, format='json').data['guid']
        response = self.client.get('api/v1/resources/guid/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'],"Funtional Geekery Episode 127")


    def test_patch_one_resource(self):
        url = '/api/v1/resources/?search=Katie Hughes'
        guid = self.client.get(url, format='json').data['guid']

        data= {
            "description": "A _diabolically irresponsible_ talk in which I celebrate modern Python coding by **abandoning all backwards compatibility** THE END",
            "tags": ["test tags", "testing"]
        }
        response = self.client.patch('api/v1/resources/guid/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['tags']["name"], data['tags'][0])


    def test_delete_one_resource(self):
        #to do:  grab the guid from the created guids in the DB instead of hard coding it.
        url = '/api/v1/resources/7a25b429-20a7-4246-a49a-c614b08bfc72/'
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
             "date_published":"2019-09-19T03:27:06Z",
             "created":"2019-09-19T03:27:06.485Z",
             "modified":"2019-09-19T03:27:06Z",
             "media_type":"WEB",
             "tags":["JavaScript", "FrontEnd"]
             }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "The Modern JavaScript Tutorial")
        self.assertEqual(response.data['other_referring_source'], "iliakan@javascript.info")
