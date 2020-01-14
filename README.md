# Django proof-of-concept for CodeBuddies V3

Background: https://github.com/codebuddies/codebuddies/issues/1136

The API spec all the proof-of-concepts: https://app.swaggerhub.com/apis-docs/billglover/CodeBuddies/0.0.1

Crowdsourced brainstorm of problems we want to solve: https://pad.riseup.net/p/BecKdThFsevRmmG_tqFa-keep

## Setup

Although it is possible to run this locally, we recommend you run CodeBuddies locally using Docker. We assume you have Docker installed, but if not head on over to the Docker [Getting Started](https://www.docker.com/products/docker-desktop) guide and install Docker Desktop for your operating system.

1. Fork this repository.
2. Clone your fork (don't forget to replace the repo URL with that of your fork).

```
git clone git@github.com:billglover/django-concept.git cb
```

3. Navigate into the project directory.

```
cd cb
```

4. Start the local development environment.

```
docker-compose up
```

This will run the following components:

* Nginx, a web server providing access to the application: http://localhost:8000
* Adminer, a front-end for PostgreSQL: http://localhost:8001
* Mailhog, a web interface for viewing all mail sent by the application: http://localhost:8025
* A PostgreSQL database: postgres://babyyoda:mysecretpassword@localhost:5432/codebuddies
* The Django web application accessible via the Nginx web server

Press Ctrl + C when you need to stop the application.

## Editing

With the local environment running, you can modify the application code in your editor of choice. As you save changes, the application should reload automatically. If you need to run database migrations, stop the running containers with Ctrl + C and then re-start with `docker-compose up`.

# Proof-of-concept Goals

A resource datastore

- save resource
- delete resource
- update resource
- list resource
- search resources

Resource:

- title
- description
- type
- credit
- url
- referrer

The start of a resource bookmarking/archiving service.

- Calendar/hangouts
  - How easy would it be to make a calendar widget that lets users block out times they're free for hangouts?

# Findings

# Technologies Used
