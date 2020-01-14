# Django proof-of-concept for CodeBuddies V3

Background: https://github.com/codebuddies/codebuddies/issues/1136

The API spec all the proof-of-concepts: https://app.swaggerhub.com/apis-docs/billglover/CodeBuddies/0.0.1

Crowdsourced brainstorm of problems we want to solve: https://pad.riseup.net/p/BecKdThFsevRmmG_tqFa-keep

# Setup

- Fork this repo
- Make sure you have Python 3 and Postgres 11.1 installed

---

You can either set up Postgres locally or using Docker.

### Set up Postgres with Docker:

[Docker](https://www.docker.com/) makes it easy to [install and manage Postgres](https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198).

With Docker installed, try the following steps:

1. `docker pull postgres`
2. `mkdir -p $HOME/docker/volumes/postgres`
3. docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres

Postgres should then be accessible via localhost, e.g. from Django or with the psql command line tool:

```psql -h localhost -U postgres -d postgres```

With the new settings file using django-environ, django will expect an env variable (either in the environment or in a .env file) called DATABASE_URL. It should take this form:

```postgres://{user}:{password}@{hostname}:{port}/{database-name}```

As an example:
```postgres://silly_username:a_password@localhost:5342/your_db_name_here```

env.db() will then parse this into a DATABASE dict automatically for Djangos use in settings.

### Set up Postgres locally:

1. Install Postgress ([using brew](https://gist.github.com/ibraheem4/ce5ccd3e4d7a65589ce84f2a3b7c23a3), if on mac)

2. Follow the steps at [https://wiki.postgresql.org/wiki/First_steps](https://wiki.postgresql.org/wiki/First_steps)

---

In the command line, run some commands to create a user, create a database, and install requirements:

- Create a user: `$ createuser --interactive --pwprompt`
- Create a database in Postgres called cbv3_django_prototype by typing `$ createdb cbv3_django_prototype`
- Type `$ pip install -r requirements.txt`

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
