from unittest import skip
from random import randint
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from users.factories import UserFactory
from resources.factories import  ResourceFactory
from factory import PostGenerationMethodCall, LazyAttribute, create, create_batch



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ResourcesTests(APITestCase):


    def setUp(self):
        self.user = UserFactory(password=PostGenerationMethodCall('set_password', 'codebuddies'))

        url = '/auth/obtain_token/'
        data = {"username": self.user.username, "password": "codebuddies"}
        token_response = self.client.post(url, data, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['token'])


    def test_view_resources(self):
        records = randint(2, 102)
        create_batch(ResourceFactory, records)

        url = '/api/v1/resources/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], records )


    def test_search_resources(self):
        create(ResourceFactory, title="Elm Crash-Course (Reactivate London)" )
        create(ResourceFactory, title="elm Documentation")
        create(ResourceFactory, description="The best place to start is the official guide. It will give you a solid foundation for creating applications with Elm. Once you have worked through that, the next place to look for documentation is on the packages you are using.")
        create(ResourceFactory, description="Elm is a programming language targeted at the front end (runs in a browser, not on Node) that offers a different take on building dynamic web applications.")

        url = '/api/v1/resources/?search=Elm'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertContains(response, "Elm Crash-Course (Reactivate London)")
        self.assertContains(response, "or creating applications with Elm. ")


    def test_view_one_resource(self):
        new_resource = create(ResourceFactory)
        url = f'/api/v1/resources/{new_resource.guid}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_resource.title)
        self.assertEqual(response.data['description'], new_resource.description)


    def test_patch_one_resource(self):
        new_resource = create(ResourceFactory)
        url = f'/api/v1/resources/{new_resource.guid}/'

        data= {
            "description": "A _diabolically irresponsible_ talk in which I celebrate modern Python coding by **abandoning all backwards compatibility** THE END",
            "author": "David Beazley",
            "tags": ["test tags", "testing", "python"]
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['author'], data['author'])
        self.assertEqual(
            sorted(item['name'] for item in response.data['tags']),
            sorted(data['tags'])
        )


    def test_delete_one_resource(self):
        records = create_batch(ResourceFactory, 10)
        new_resource = create(ResourceFactory)
        url = f'/api/v1/resources/{new_resource.guid}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        subsequent_response = self.client.get(url)
        self.assertEqual(subsequent_response.status_code, status.HTTP_404_NOT_FOUND)

        count_check = self.client.get('/api/v1/resources/')
        self.assertEqual(count_check.data['count'], 10)


    @skip('https://github.com/codebuddies/backend/issues/125')
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
                     "tags": ["JavaScript", "FrontEnd"]
             }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "The Modern JavaScript Tutorial")
        self.assertEqual(response.data['other_referring_source'], "iliakan@javascript.info")
        self.assertEqual(response.data['media_type'], 'WEB')
