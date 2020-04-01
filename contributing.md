## **Setup**

Although it is possible to run the website locally, we recommend you run CodeBuddies locally using [Docker](https://www.docker.com/get-started).

These instructions have been used on the following operating systems:  
* Linux
* Mac OS
* Windows 10 Pro

  Please note that Windows 10 Home is not supported by Docker Desktop at this time

  Docker is expected to be installed before the website is deployed. Follow the guide [here](https://www.docker.com/products/docker-desktop) to install it if you have not done so

#### Steps
1. Fork this repository. See [Fork a repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) for help if needed.   
2. Clone your fork. This creates a copy on your local computer.
  For more help see [Cloning a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

 For Mac OS or Linux
 ```plain
 git clone git@github.com::codebuddies/backend.git cb-backend
 ```
 For Windows follow the instructions on the Cloning a repository link above

 We name the folder *cb-backend* but you can change the folder name you desire

3. Navigate into the project directory
  ```plain
  cd cb-backend
  ```
4. Start the local development environment (for Windows user please ensure your docker is up running)
  ```plain
  docker-compose up -d
  ```
  This will run the following components:
  * Nginx, a web server: http://localhost:8000
  * Adminer, a DB front-end: http://localhost:8001
  * Mailhog, a dummy mailbox: http://localhost:8025
  * A PostgreSQL database
  * Django web application

  You can view the application or make API calls by using the Nginx URL.

  You can access the database through the Adminer front-end or using a local PostgreSQL client and the following URL:
  ```plain
  postgres://babyyoda:mysecretpassword@localhost:5432/codebuddies
  ```
  ![screenshot of Adminer](https://i.imgur.com/Dtg5Yel.png)  

  To stop the application and remove all containers, run the following  
  ```plain
  docker-compose down
  ```

5. Create a superuser so that you can log into http://localhost:8000/admin by running the following in your terminal:  
  ```plain
  docker-compose run --rm app ./manage.py createsuperuser
  ```

### Editing the Code

  With the local environment running, you can modify the application code in your editor of choice. As you save changes, the application should reload automatically. There should be no need to restart container to see code changes.


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

  To tail logs in console, remove the detach flag `-d` from `docker-compose up` command when you start the application
