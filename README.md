# Django proof-of-concept for CodeBuddies V3

Background: https://github.com/codebuddies/codebuddies/issues/1136

The API spec all the proof-of-concepts: https://app.swaggerhub.com/apis-docs/billglover/CodeBuddies/0.0.1

Crowdsourced brainstorm of problems we want to solve: https://pad.riseup.net/p/BecKdThFsevRmmG_tqFa-keep

## Setup

Although it is possible to run this locally, we recommend you run CodeBuddies locally using Docker. We assume you have Docker installed, but if not head on over to the Docker [Getting Started](https://www.docker.com/products/docker-desktop) guide and install Docker for your operating system.

These instructions have been used on the following operating systems.

* Linux
* Mac OS
* Windows 10 Pro

Please note that Windows 10 Home is not supported by Docker Desktop at this time.

1. Fork this repository. This creates a copy of the repository for you to work on. For more help see this GitHub guide: [Fork a repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo).
2. Clone your fork. This creates a copy on your local computer. For more help see this GitHub guide: [Cloning a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

```plain
git clone git@github.com:codebuddies/django-concept.git cb
```

3. Navigate into the project directory.

```plain
cd cb
```

4. Start the local development environment.

```plain
docker-compose up -d
```

This will run the following components:

- Nginx, a web server: http://localhost:8000
- Adminer, a DB front-end: http://localhost:8001
- Mailhog, a dummy mailbox: http://localhost:8025
- A PostgreSQL database
- The Django web application

You can view the application or make API calls by using the Nginx URL.

You can access the database through the Adminer front-end or using a local PostgreSQL client and the following URL: `postgres://babyyoda:mysecretpassword@localhost:5432/codebuddies`.

![screenshot of Adminer](https://i.imgur.com/Dtg5Yel.png)

To stop the application and remove all containers, run the following.

```plain
docker-compose down
```

5. Create a superuser so that you can log into http://localhost:8000/admin by running the following in your terminal: `$ docker-compose run --rm manage createsuperuser`

## Editing Code

With the local environment running, you can modify the application code in your editor of choice. As you save changes, the application should reload automatically. There should be no need to restart containers to see code changes.

## Other Tasks

### Logs

View logs from all containers.

```plain
docker-compose logs
```

View logs from a single container (in this case the `app` container).

```plain
docker-compose logs app
```

You can use the same structure to view logs for the other containers; `nginx`, `db`, `mailhog`, `adminer`, `app`.

If you would like to tail the logs in the console then you remove the detach flag, `-d`, from the `docker-compose up` command that you use to start the application.

### Django Management

The following are examples of some common Django management commands that you may need to run.

* Make Migrations: `docker-compose run --rm manage makemigrations`
* Merge Migrations: `docker-compose run --rm manage makemigrations --merge`
* Run Migrations: `docker-compose run --rm manage`
* Test: `docker-compose run --rm manage test`

To see the full list of management commands use `help`.

```plain
docker-compose run --rm manage help
```

## Removing Everything

To remove all containers run the following:

```plain
docker-compose rm
```

This will leave a copy of the data volume (holding the PostgreSQL data) behind. To remove that you will need to identify and remove the data volume.

```plain
docker volume ls

DRIVER              VOLUME NAME
local               django-concept_db_data
```

Note the name of the data volume, in this case `django-concept_db_data` and delete it.

```plain
docker volume rm django-concept_db_data
```

Note: it is likely that cached copies of your container images will be retained by Docker on your local machine. This is done to speed things up if you require these images in future. To completely remove unused container images and networks, we recommend you follow Docker [pruning guide](https://docs.docker.com/config/pruning/).

## Proof-of-concept Goals

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
