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

[https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198](https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198)

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
