![Test](https://github.com/codebuddies/django-concept/workflows/Test/badge.svg)
[![codecov](https://codecov.io/gh/codebuddies/backend/branch/master/graph/badge.svg)](https://codecov.io/gh/codebuddies/backend)

## Overview of CodeBuddies
CodeBuddies is a remote-first community of independent code learners who enjoy sharing knowledge and helping each other learn faster via discussions and pairing. It is free and open-sourced, and supported by open source contributors and financial backers on our [Open Collective](https://opencollective.com/codebuddies). 
 
We are building out a new platform (codebuddies version 3 - cbv3) to replace the old website at at [codebuddies.org](https://codebuddies.org).
 
The new version of the website will include features that will help users:
share and recommend links to resources/tutorials
find open source projects to work on
form study groups 
collect learning paths and share them
find 1-hour pair programming partners for any topic much more easily


**Note:** This project is currently _in development_

**Note:** The production branch of this repo is called `main` [to support the black lives matters movement]

## Code of Conduct
We expect contributors to follow our [code of conduct](https://codebuddies.org/slack). 

## Role of the Backend
The backend is a Django app that provides API endpoints that the frontend (a React app) consumes. 

We have a technical decision log [here](https://github.com/codebuddies/backend/wiki/Decision-log), and we document technical discussions and learnings in the [discussions tab](https://github.com/codebuddies/backend/discussions). 

## Front End
The front-end repo is built using React and is located at [github.com/codebuddies/frontend](https://github.com/codebuddies/frontend). Until a staging-api.codebuddies.org URL is live, contributors need to have this backend app running locally (localhost:8000) in order to develop on the front-end.

## Tech used
The backend uses Django built on top of [Cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.0/) and [Django Rest Framework](https://www.django-rest-framework.org/).

We use Docker Compose to stand up local development environments, and GitHub Actions to deploy staging and production. We host on DigitalOcean and store everything in a managed PostgreSQL database.

Some core dependencies we use:
djangorestframework==3.10.2   # https://github.com/encode/django-rest-framework
coreapi==2.3.3                # https://github.com/core-api/python-client
drf-jwt==1.13.4               # https://github.com/Styria-Digital/django-rest-framework-jwt

## Contributing & Development Environment Set-Up

Please see [CONTRIBUTING.MD]

## Get Help
Ways you can get help if you're stuck or have questions:
-[ ] Create a new [discussion](https://github.com/codebuddies/backend/discussions) post with your question
-[ ] Ask in the #codebuddies-meta channel on the CodeBuddies Slack (see: codebuddies.org/slack)

## Other Ways to Contribute
There are other ways to contribute to CodeBuddies besides making pull requests to the codebase! 

You can:
[x] participate in the community on Slack
[x] share your feedback on GitHub issues or discussions
[x] help review pull requests by checking out the branch and affirming that the expected changes are there

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

## Proof-of-concept Goals

[MVP Progress tracker board](https://github.com/codebuddies/backend/projects/1)

1. A resource datastore

- [x] save resource
- [x] delete resource
- [x] update resource
- [x] list resource
- [x] search resources

2. Resource:

- [x] title
- [x] description
- [x] type
- [x] credit
- [x] url
- [x] referrer

3. Authentication

## Reference Links

- [Original Discussion]
- [CBV3 tech notes doc] (note: we're moving technical discussion to the new [discussion tab](https://github.com/codebuddies/backend/discussions).
- [API spec draft on Swaggerhub]
- [Front-end decision log]
- [Back-end decision log]
- [Crowdsourced brainstorm of problems we want to solve]

<!-- TODO: # Findings -->

<!-- TODO: # Technologies Used -->

<!-- What codebuddies is building links: -->
[Original Discussion]: https://github.com/codebuddies/codebuddies/issues/1136
[CBV3 tech notes doc]: https://docs.google.com/document/d/1YuVO-v0n73ogoFIwpwJgI1Bkso8sP2mg5zqbX9FB3lU/edit
[Crowdsourced brainstorm of problems we want to solve]: https://pad.riseup.net/p/BecKdThFsevRmmG_tqFa-keep

<!-- Contribution links -->
[CONTRIBUTING.MD]: https://github.com/codebuddies/backend/blob/main/contributing.md
[See PR 127]: https://github.com/codebuddies/backend/issues/127

<!-- Howto links -->
[Cloning a repository]: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository
[Fork a repo]: https://help.github.com/en/github/getting-started-with-github/fork-a-repo
[Getting Started]: https://www.docker.com/products/docker-desktop

<!-- Spec links -->
[API spec draft on Swaggerhub]: https://app.swaggerhub.com/apis-docs/billglover/CodeBuddies/0.0.1
[Front-end decision log]: https://github.com/codebuddies/frontend/wiki/Technical-decision-log
[Back-end decision log]: https://github.com/codebuddies/backend/wiki/Decision-log

<!-- Reference links -->
[CodeBuddies V3 Back-end]: https://github.com/codebuddies/backend
[Codebuddies V3 Front-end]: https://github.com/codebuddies/frontend

[to support the black lives matters movement]: https://www.zdnet.com/article/github-to-replace-master-with-alternative-term-to-avoid-slavery-references/
