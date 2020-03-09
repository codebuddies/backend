[//]: <> (github.com/codebuddies/backend/)
## **Overview of Codebuddies**

### What is CodeBuddies?
[CodeBuddies](https://codebuddies.org/) is a remote-first community of independent code learners who enjoy sharing knowledge and helping each other learn faster via discussions and pairing. It is free and open-sourced, and supported by open source contributors and financial backers on our [Open Collective](https://opencollective.com/codebuddies).  

### CodeBuddies website Version 3 (CBV3)

We are currently building out a new platform (CBV3) to replace the [old version](http://github.com/codebuddies/codebuddies) which is currently shown at [codebuddies.org]((https://codebuddies.org/)).  

The new version of the website will include features that will help users:
* share and recommend resources/tutorial links
* find open source projects to work on
* form study groups
* collect learning paths and share them
* pair programming -- find 1-hour pair programming partners for any topics in a much more easier way

## **Role of Backend**
The backend of CBV3 is an app which is composed of Django REST Framework that provides API endpoints which the frontend app (React) consumes.

We have a technical decision log [here](https://github.com/codebuddies/backend/wiki/Decision-log).

## **Links to Clients / Frontend**
The frontend of CBV3 is built with React and is located at [here](http://github.com/codebuddies/frontend).

## **Technology Used**
Components of the CBV3 Backend:
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.0/)

Application Deployment
* [Docker Compose](http://docs.docker.com/compose) to stand up local development environments
* [Github Actions](http://help.github.com/en/actions) to deploy staging and production.

Database:
* [PostgreSQL](http://postgresql.org)
* [DigialOcean Droplets](http://digitalocean.com/products/droplets) to store the database on cloud

Core dependencies of CBV3
| Dependencies | Version | Github Link |
| ------------ | :-----: | ----------- |
| djangorestframework | 3.10.2 | https://github.com/encode/django-rest-framework |
| coreapi | 2.3.3 | https://github.com/core-api/python-client
| drf-jwt | 1.13.4 | https://githbu.com/Styria-Digital/django-rest-framework-jwt |

## **Can I run the website application on my computer?**
Of course you can. Follow the [instruction](contributing.md) to set up the Django API backend.
Set up using Docker is highly recommended.

## **Have Questions about CBV3?**
Check out [support.md](support.md) if you're stuck or have questions.

## **Ways to Get Involved**
Anyone is welcome to contribute and make the website better! You can:
* Join our slack community by following the [instruction](https://codebuddies.org/slack) on how to join.

## **CODE_OF_CONDUCT.md**
