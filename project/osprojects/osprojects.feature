Feature: Create views for the new Projects API Endpoint.
# Some of these items may not need custom code, but are listed here as a reminder of what's needed:

    Scenario: Create list and detail views for the endpoint.
    # See the DRF ModelViewSet, DRF Generic Views and DRF CreateModelMixin for background and places to start.

    Scenario: Add an ISAuthenticated permissions class to require a login for the endpoint.
    # See Permissions in DRF

    Scenario: Add search or filter backends as needed.
    # See DB queries in Django, DRF Filter Backends, Filtering in DRF, and DRF SearchFilter for some background to start.

    Scenario: Add search_fields for endpoint

    Scenario: Add PATCH function to update records already in the DB

    Scenario: Add perform create function as needed for specialized user lookup or other (e.g. many-to-many) relations.

    Scenario: Add/define queryset for the list view of projects

    Scenario: Add links to associated serializers

# Tests(?)
## On POST:
    - For a given set of dummy data for the Projects model, return JSON string with all available projects.
    - For a given set of dummy data for the Projects model, return JSON string for the Projects guid.

NOTES:
    - Endpoints, test to check that each endpoint exists
    - Test that a specific Projects endpoint gives back desired data/matches data we expect.
    - Test that authenticated-only users can create a new project API endpoint.

    - 'Evil user tests': test what happens if user deliberately breaks CRUD API actions on Projects Endpoints
    - Write test in way that we know are going to fail, make a checklist_id?
    - Confirm 200 server code for an api endpoint instance.