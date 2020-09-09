import pytest
from .factories import OSProjectsFactory


@pytest.mark.django_db
def test_osprojects_model():
    """ Test OSProjects model """
    # create OSProjects model instance
    osproject = OSProjectsFactory(title="Buddybot", guid="cc63f918-d515-11ea-956f-0242ac130002")
    assert osproject.title == "Buddybot"
    assert osproject.guid == "cc63f918-d515-11ea-956f-0242ac130002"
