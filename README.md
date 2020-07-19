# [CodeBuddies V3 Back-end]
## Django proof-of-concept

![Test](https://github.com/codebuddies/django-concept/workflows/Test/badge.svg)
[![codecov](https://codecov.io/gh/codebuddies/backend/branch/master/graph/badge.svg)](https://codecov.io/gh/codebuddies/backend)

**Note:** This project is currently _in development_

## Sponsors

Big thanks to the sponsors of this project!

<a href="https://opencollective.com/codebuddies/sponsor/0/website" target="_blank"><img src="https://opencollective.com/codebuddies/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/codebuddies/sponsor/1/website" target="_blank"><img src="https://opencollective.com/codebuddies/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/codebuddies/sponsor/2/website" target="_blank"><img src="https://opencollective.com/codebuddies/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/codebuddies/sponsor/3/website" target="_blank"><img src="https://opencollective.com/codebuddies/sponsor/3/avatar.svg"></a>

<a href="https://gitduck.com/codebuddies/join?t=60ktFkh1Rqnd_AS1kR8ZGyH" target="_blank">Join CodeBuddies on GitDuck</a>

## Features

- **Auto-reload** - modify the application code in your editor of choice. As you save changes, the application should reload automatically. There should be no need to restart containers to see code changes.
<!-- TODO -->

## Reference

- [Background]
- [The API spec all the proof-of-concept]
- [Crowdsourced brainstorm of problems we want to solve]
- Will interact as the API supporting the [Codebuddies V3 Front-end]

## Getting started

We recommend you run CodeBuddies locally using Docker. We assume you have Docker installed, but if not head on over to the Docker [Getting Started] guide and install Docker for your operating system.

These instructions have been used on the following operating systems.

- Linux
- Mac OS
- Windows 10 Pro - Please note that Windows 10 Home is not supported by Docker Desktop at this time.

1. Fork this repository. This creates a copy of the repository for you to work on. For more help see this GitHub guide: [Fork a repo].
2. Clone your fork. This creates a copy on your local computer. For more help see this GitHub guide: [Cloning a repository].

```bash
$ git clone https://github.com/codebuddies/backend codebuddies-backend
```

3. Navigate into the project directory.

```bash
$ cd codebuddies-backend
```

4. Start the local development environment.

```bash
$ docker-compose up -d
```

**Note:** `-d` starts Docker in detatched mode. See [logs](#debugging-with-docker-logs)

### Local development environment details

This will run the following components:

- Nginx, a web server: http://localhost:8000 - view the application or make API calls
- Mailhog, a dummy mailbox: http://localhost:8025
- The Django web application
- Adminer, a DB front-end: http://localhost:8001
- A PostgreSQL database `postgres://babyyoda:mysecretpassword@localhost:5432/codebuddies`

You can access the database through the Adminer front-end or using a local PostgreSQL client

![screenshot of Adminer](https://i.imgur.com/Dtg5Yel.png =250x)

5. Create a superuser so that you can log into `http://localhost:8000/admin` by running the following in your terminal:

```bash
$ docker-compose run --rm app ./manage.py createsuperuser
```

6. You can populate the database with some random test data for development purposes by running

```bash
$ docker-compose run --rm app ./manage.py init_data
```

All user accounts created by this command have the password `codebuddies`.

See the `init_data --help` command for more information:

```bash
$ docker-compose run --rm app ./manage.py init_data --help

usage: manage.py init_data [-h] [--clear-db] [--num-users NUM-USERS]
                           [--num-tags NUM-TAGS]
                           [--num-resources NUM-RESOURCES] [--version]
                           [-v {0,1,2,3}] [--settings SETTINGS]
                           [--pythonpath PYTHONPATH] [--traceback]
                           [--no-color] [--force-color]

Initialize the DB with some random fake data for testing and development

optional arguments:
  --clear-db            Clear existing data from the DB before creating test
                        data
  --num-users NUM-USERS
                        Number of `User` objects to create (default 10)
  --num-tags NUM-TAGS   Number of `Tag` objects to create (default 10)
  --num-resources NUM-RESOURCES
                        Number of `Resource` objects to create (default 10)
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
```

[See PR 127]

---

To stop the application and remove all containers, run the following:


```bash
$ docker-compose down
```

## Other Tasks

### Automated Tests

- We use [pytest](https://docs.pytest.org/en/latest/contents.html) with the [pytest-django](https://pytest-django.readthedocs.io/en/latest/) plugin for running tests.
- Please add tests for your code when contributing.
- Run the test suite using `docker-compose run --rm app pytest`
- With test coverage report `docker-compose run --rm app pytest --cov-report=term --cov=.`

### Debugging with Docker Logs

View logs from all containers.

```bash
$ docker-compose logs
```

View logs from a single container (in this case the `app` container).

```bash
$ docker-compose logs app
```

You can use the same structure to view logs for the other containers; `nginx`, `db`, `mailhog`, `adminer`, `app`.

If you would like to tail the logs in the console then you remove the detach flag, `-d`, from the `docker-compose up` command that you use to start the application.

### Django Management

The following are examples of some common Django management commands that you may need to run.

- Make Migrations: `docker-compose run --rm app ./manage.py makemigrations`
- Merge Migrations: `docker-compose run --rm app ./manage.py makemigrations --merge`
- Run Migrations: `docker-compose run --rm app ./manage.py migrate`

To see the full list of management commands use `help`.

```plain
docker-compose run --rm app ./manage.py help
```

### Postman

<details>
<summary>Importing Postman collection</summary>
<br>
Postman is a free interactive tool for verifying the APIs of your project. You can download it at postman.com/downloads.

Postman is an interactive tool for verifying the APIs of your project in an isolated environment--think of it as a a virtual playground where we can safely experiment and edit our API before we deploy it on our web app--just like virtual environments help us isolate our python dependencies.

We've created a shared Postman collection (a .json file) in the postman folder to help contributors more easily reproduce observed behaviour in our dev API.

To get it set up, please follow these steps:

1. Download Postman

Downloading Postman
Please make sure it is at least v7.6.0, if installed, or you are downloading the latest stable version.
Linux,

- Distro package manager:
- use the search feature to find in your package manager
- (RECOMMENDED) Flatpak
- After setting up flatpak it through flatpak using flatpak install postman and enter "yes"/"y" for all the questions it will ask. Flatpak is designed to provide the most up-to-date versions of software for most distros, so if you have the option, use Flatpak to guarantee Linux OS compatibility and to keep Postman up-to-date.

2. Once you have Postman open, click on file -> import and import the .json file
3. Click on the settings gear icon on the far top right (next to the eye icon) and click to add a new environment.
4. Name your environment `dev` and create a variable called `api_url`. Give it a value of `https://localhost:8000`, which is the URL of your Django dev environment when it is running.
5. Now, as long you have the Django app (https://localhost:8000) running, you should be able to make requests like POST Create User and POST Authenticate.
   Click on this link to see what you should expect: https://imgur.com/hd9VB6k

- `POST` Create User will create a new user in your `localhost:8000` running Django app,
- making a request to `POST Authenticate` will authenticate whether or not that user exists.

![screenshot of Postman environment variable setup](https://i.imgur.com/6Uq9XQp.png)

5. Now, as long you have the Django app (https://localhost:8000) running, you should be able to make requests like `POST Create User` and `POST Authenticate` by clicking on the blue "Send" button in Postman.

</details>

## Removing Everything

<details>
<summary>To remove all containers</summary>
<br>
To remove all containers run the following:

```bash
$ docker-compose rm
```

This will leave a copy of the data volume (holding the PostgreSQL data) behind. To remove that you will need to identify and remove the data volume.

```bash
$ docker volume ls

DRIVER              VOLUME NAME
local               django-concept_db_data
```

Note the name of the data volume, in this case `django-concept_db_data` and delete it.

```bash
$ docker volume rm django-concept_db_data
```

**Note:** it is likely that cached copies of your container images will be retained by Docker on your local machine. This is done to speed things up if you require these images in future. To completely remove unused container images and networks, we recommend you follow Docker [pruning guide](https://docs.docker.com/config/pruning/).

</details>

## Proof-of-concept Goals

A resource datastore

- [x] save resource
- [x] delete resource
- [x] update resource
- [x] list resource
- [x] search resources

Resource:

- [x] title
- [x] description
- [x] type
- [x] credit
- [x] url
- [x] referrer

The start of a resource bookmarking/archiving service.

- [ ] Calendar/hangouts
  - How easy would it be to make a calendar widget that lets users block out times they're free for hangouts?

## Contributing

Please see [How to contribute here]

## Spec docs

- [CBV3 tech notes doc]
- [The API spec all the proof-of-concept]
- [Front-end decision log]
- [Back-end decision log]

<!-- TODO: # Findings -->

<!-- TODO: # Technologies Used -->

<!-- What codebuddies is building links: -->
[Background]: https://github.com/codebuddies/codebuddies/issues/1136
[CBV3 tech notes doc]: https://docs.google.com/document/d/1YuVO-v0n73ogoFIwpwJgI1Bkso8sP2mg5zqbX9FB3lU/edit
[Crowdsourced brainstorm of problems we want to solve]: https://pad.riseup.net/p/BecKdThFsevRmmG_tqFa-keep

<!-- Contribution links -->
[How to contribute here]: https://github.com/codebuddies/django-concept/wiki/Contribution-instructions
[See PR 127]: https://github.com/codebuddies/backend/issues/127

<!-- Howto links -->
[Cloning a repository]: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository
[Fork a repo]: https://help.github.com/en/github/getting-started-with-github/fork-a-repo
[Getting Started]: https://www.docker.com/products/docker-desktop

<!-- Spec links -->
[The API spec all the proof-of-concept]: https://app.swaggerhub.com/apis-docs/billglover/CodeBuddies/0.0.1
[Front-end decision log]: https://github.com/codebuddies/frontend/wiki/Technical-decision-log
[Back-end decision log]: https://github.com/codebuddies/backend/wiki/Decision-log

<!-- Reference links -->
[CodeBuddies V3 Back-end]: https://github.com/codebuddies/backend
[Codebuddies V3 Front-end]: https://github.com/codebuddies/frontend
