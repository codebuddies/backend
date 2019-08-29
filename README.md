# Django proof-of-concept for CodeBuddies V3

Background: https://github.com/codebuddies/codebuddies/issues/1136

Crowdsourced brainstorm of problems we want to solve: https://pad.riseup.net/p/BecKdThFsevRmmG_tqFa-keep

# Setup
- Make sure you have Postgres 11.1 installed
- Create a Postgres user by typing `createuser --interactive --pwprompt`
- Create a database in Postgres called cbv3_django_prototype by typing `createdb cbv3_django_prototype`
- Type `pip install -r requirements.txt` in your command line

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


