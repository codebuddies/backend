## Getting started

We recommend you run CodeBuddies locally using Docker. We assume you have Docker installed, but if not please [install Docker for your operating system](https://docs.docker.com/desktop/). 

These instructions have been used on the following operating systems.

- [Linux Docker installation guide](https://docs.docker.com/engine/install/ubuntu/)
- [Mac OS Docker installation guide](https://docs.docker.com/docker-for-mac/install/)
- [Windows 10 Pro Docker installion guide](https://docs.docker.com/docker-for-windows/install/)
- [Windows 10 Home Docker installation guide](https://docs.docker.com/docker-for-windows/install-windows-home/)

## Development Environment Setup 
1. Fork this repository. This creates a copy of the repository for you to work on. For more help see this GitHub guide: [Fork a repo].

2. Clone your fork. This creates a copy on your local computer. For more help see this GitHub guide: [Cloning a repository].

```bash
$ git clone https://github.com/codebuddies/backend codebuddies-backend
```

3. Navigate into the project directory.

```bash
$ cd codebuddies-backend
```

4. Run the following docker command to start up the local development environment.

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
$ docker-compose run --rm app python ./manage.py createsuperuser
```

6. You can populate the database with some random test data for development purposes by running

```bash
$ docker-compose run --rm app python ./manage.py init_data
```

All user accounts created by this command have the password `codebuddies`.

See the `init_data --help` command for more information:

```bash
$ docker-compose run --rm app python ./manage.py init_data --help

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

Migrations are Django's way of propogating model changes into the database schema (([doc](https://docs.djangoproject.com/en/3.1/topics/migrations/)). 

Whenever you made a change to a model file*, you should run `docker-compose run --rm app python ./manage.py makemigrations` and `docker-compose run --rm app python ./manage.py migrate` in order to update the models for the database. 

A PR reviewer should see the associated migration files in the PR diff when there is a model change.


The following list contains some common Django management commands that you may need to run.

- Make Migrations: `docker-compose run --rm app python ./manage.py makemigrations`
- Merge Migrations: `docker-compose run --rm app python ./manage.py makemigrations --merge`
- Run Migrations: `docker-compose run --rm app python ./manage.py migrate`
- Make sure new packages are installed: `docker-compose up -d --build`

To see the full list of management commands use `help`.

```plain
docker-compose run --rm app python ./manage.py help
```

*Examples of changes to model files:

PK changes
removals
fieldname changes
multiple sets of changes with reversions
datatype changes

You should be double checking their migration files and consolidating, organizing, and deleting excess where necessary.

Only the migration files that make the final intended changes should be checked in (e.g. the final field name in its migration, or the final PK change in its migration). 


### Editing the Code

  With the local environment running, you can modify the application code in your editor of choice. As you save changes, the application should reload automatically. There should be no need to restart container to see code changes.

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
4. Name your environment `dev` and create a variable called `api_url`.  For both the "Initial Value" and "Current Value," fill in `http://localhost:8000` which is the URL of your Django dev environment when it is running.
5. Now, as long you have the Django app (http://localhost:8000) running, you should be able to make requests like POST Create User and POST Authenticate.
   Click on this link to see what you should expect: https://imgur.com/hd9VB6k

- `POST` Create User will create a new user in your `localhost:8000` running Django app,
- making a request to `POST Authenticate` will authenticate whether or not that user exists.

![screenshot of Postman environment variable setup](https://user-images.githubusercontent.com/4512699/88751261-14fa9280-d10c-11ea-80c4-2934c27254ad.png)

5. Now, as long you have the Django app (http://localhost:8000) running, you should be able to make requests like `POST Create User` and `POST Authenticate` by clicking on the blue "Send" button in Postman.

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

## Getting Help
Ways you can get help if you're stuck or have questions: 

-[x] Create a [new discussion post](https://github.com/codebuddies/backend/discussions) with your question 

-[x] Ask in the #codebuddies-meta channel on the CodeBuddies Slack (see: [codebuddies.org/slack](https://codebuddies.org/slack)
