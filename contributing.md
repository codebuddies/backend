## **Contributing CodeBuddies website version 3 (CBV3)**

## **Setup**

Although it is possible to run the website locally, we recommend you run CodeBuddies locally using [Docker](https://www.docker.com/get-started).  

These instructions have been used on the following operating systems:  
* Linux
* Mac OS
* Windows 10 Pro (Windows 10 Home is supported by Docker Desktop at the moment)

### Prerequisites

  Contributors are expected to have fundamental knowledge of the [technologies used for CBV3](README.md#technologies-used).
  (recommendations of tutorials?)

#### Steps

Docker is expected to be installed before the website is deployed. Follow the guide [here](https://www.docker.com/products/docker-desktop) to install it if you have not done so

1. Fork this repository. See [Fork a repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) for help if needed.   
2. Clone your fork.

  ```plain
  git clone git@github.com::codebuddies/backend.git cb-backend
  ```
  Clone the forked repository to your computer using the command `git clone` and save as `cb-backend`. This command works on MacOS and Linux. For details or Windows user, follow the instructions on [Cloning a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

3. Navigate into the project directory
  ```plain
  cd cb-backend
  ```

4. Start the local development environment

  (for Windows user please ensure your docker is up running)

  ```plain
  docker-compose up -d
  ```

  This will run the following components:
  * Nginx, a web server: http://localhost:8000
  * Adminer, a DB front-end: http://localhost:8001
  * Mailhog, a dummy mailbox: http://localhost:8025
  * A PostgreSQL database
  * Django web application   


  * __Web Server (Nginx)__  
    You can view the application or make API calls by using the Nginx URL

  * __Accessing Database (Adminer)__  
    You can access the database through the Adminer front-end or using a loca PostgreSQL client with the following command:

    ```plain
    postgres://babyyoda:mysecretpassword@localhost:5432/codebuddies
    ```      

5. Create a superuser so that you can log into http://localhost:8000/admin by running the following in your terminal:  
  ```plain
  docker-compose run --rm app ./manage.py createsuperuser
  ```

  ![screenshot of Adminer](https://i.imgur.com/Dtg5Yel.png)  

To stop the application and remove all containers, run the following  
  ```plain
  docker-compose down
  ```

### Editing the Code

  With the local environment running, you can modify the application code in your editor of choice. As you save changes, the application should reload automatically. There should be no need to restart container to see code changes.

## **Django Management via Docker**

  Notes: The following commands are only applicable to MacOS and Linux.

  __Common Commands for Managing Django project__

  Majority of the Django manage.py commands can also be applied through docker. Below are some examples:

  * Access Python shell (IPython): `docker-compose run --rm manage shell`
  * Run test: `docker-compose run --rm manage test`

  See the full list of commands: `docker-compose run --rm manage help`

  __Migrating Models__

  If any changes are made on the project models, we will need to migrate it to apply the changes. See [Django Migration](https://docs.djangoproject.com/en/3.0/topics/migrations/) for details.

  Steps to apply migrations via docker:
  1. Make migrations: `docker-compose run --rm manage makemigrations`
  2. Apply migrations: `docker-compose run --rm manage migrate`

  Merge migrations: `docker-compose run --rm manage makemigrations --merge`

## Other Tasks

### Logs
  View logs from all containers

  ```plain
  docker-compose logs
  ```
  View logs from a single container (in this case the `app` container)
  ```plain
  docker-compose logs app
  ```
  You can use the same structure to view logs for the other containers: `nginx`, `db`, `mailhog`, `adminer`, `app`

  To tail logs in console, remove the detach flag `-d` from `docker-compose up` command when you start the application.

## **Import Postman Collection**
Postman is a free interactive tool for verifying the APIs of your project in an isolated environment -- think of it as a virtual playground where we can safely experience and edit our API before we deploy it on your web app -- just like virtual envrionments help us isolate our python dependencies. You can download it at [postman.com/downloads](http://postman.com/downloads).

We've created a shared Postman collection (a .json file) in the postman folder to help contributors more easily reproduce observed behaviour in our dev API.

### Setup

1. Downloading Postman

Please ensure the installed version is later than v7.6.0 if you have previously installed the program.

(linux)?

  - Distro package manager:
    use the search feature to find in your package manager  
    (RECOMMENDED) Flatpak
  After setting up flatpak it through flatpak using flatpack install postman and enter "yes"/"y" for all the questions it will ask. Flatpak is designed to provide the most up-to-date versions of software for most distros, so if you have the option, use Flatpak to guarantee Linux OS compatibility and to keep Postman up-to-date.

  2. open Postman, click on file -> import -> import the .json file
  3. Click the settings gear icon on the far top right (next to the eye icon) and click to add a new environment.
  4. name your environment `dev` and create a variable call `api_url`. Give it a value of `https://localhost:8000`, which is the URL of your Django dev environment when it is running.
  5. Now, as long as you have the Django app (https://localhost:8000) running, you should be able to make requests like POST Create User and POST Authenticate. Click on this link to see what you should expect: https://imgur.com/hd9VB6k

5. Now, as long you have the Django app (https://localhost:8000) running, you should be able to make requests like `POST Create User` and `POST Authenticate` by clicking on the blue "Send" button in Postman.

  POST Create User will create a new user in your localhost:8000 running Django app, and making a request to POST Authenticate will authenticate whether or not that user exists.

  ![screenshot of Postman environment variable setup](https://i.imgur.com/6Uq9XQp.png)


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
  =======
  Please see [instructions here](https://github.com/codebuddies/django-concept/wiki/Contribution-instructions)

  This project is not deployed yet, but will interact as the API supporting [https://github.com/codebuddies/frontend](https://github.com/codebuddies/frontend)
