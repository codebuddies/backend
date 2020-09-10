from django.test import TestCase
from rest_framework import status

# return 200 for success create api post from projects page
def test_create_one_project(self):
    url = "/api/v1/osprojects/"
    data = {
        "guid": "1b7d1a81-7fc5-40e7-b4e8-9621320384f2",
        "title": "This is my cool new project",
        "project_creator": "Peabody",
        "description": "This cool new project does cool new stuff",
        "url": "www.thiscoolprojecthere.com",
        "user": "peabodyperson",
        "created": "2020-05-02T03:27:06.485Z",
        "modified": "2020-05-02T03:27:06.485Z",
        "open_to_contributors": true,
        "tags": ["cool", "projects", "open", "source"],
    }

    response = self.client.post(url, data, format="json")
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(
        response.data["guid"], "1b7d1a81-7fc5-40e7-b4e8-9621320384f2",
    )
    self.assertEqual(
        response.data["title"], "This is my cool new project",
    )
    self.assertEqual(
        response.data["project_creator"], "Peabody",
    )
    self.assertEqual(
        response.data["created"], "2020-05-02T03:27:06.485Z",
    )

