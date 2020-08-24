## What type of PR is this? (check all applicable)

- [ ] ♻️ Refactor
- [ ] ✨ Feature (e.g. API change)
- [ ] 🐛 Bug Fix
- [ ] 🎨 Enhancement
- [ ] 📝 Documentation Update
- [ ] 🔖 Release
- [ ] 🚩 Other

## Context

**_Placeholder example below:_**

Closes Issue #128

Right now, on the front-end, we need to pass in a token (i.e. the user needs to be logged in) before they can see a list of resource.

```
 axios
      .get('/api/v1/resources', {
        headers: {
          Authorization: `Bearer ${authContext.authTokens.token}`,
        },
      })
```

This should be true for when users are creating a resource, but the list of resources on https://cb-react-concept.netlify.com/resources should be available to the public.

## Other Related Tickets & Documents (as needed)

**_Placeholder example:_** This relates to issue #23, and I also filed issue #43 as a next step to do after this PR is merged.

## Implementation Details
What was your thought process as you changed the code? What does someone need to consider in reviewing it?

Placeholder example:

Placeholder example:
[x] Made GET /resources not protected by authorization
[x] Changed setup for tests to make sure we're not authed for the GET requests, but are authed for POST, PATCH, and search.
[x] Added test to make sure GET /api/v1/resources/{{guid}}/ and GET /api/v1/resources/ requests and search work without a token
[x] Altered tests for GET GET /api/v1/resources/{{guid}}/ and GET /api/v1/resources/ requests and search to ensure that they also work with a token
[x] Added tests to make sure PATCH and POST fail without a token
[x] Added test to make sure DEL fails without a token

## New Libraries/Dependancies Introduced (Fill out as needed)


If you have added libraries or other dependancies, please list them (and links to their repos) below:

- [ ] I've updated `requirements.txt`

## Any new migration files added?

- [ ] 👍 yes
- [ ] 🙅 no, because they aren't needed

## Did you add tests?
**_Code added or changed without test coverage or good reason for exemption won't be approved._**

- [ ] 👍 yes
- [ ] 🙋 no, because I need help
- [ ] 🙅 no, because they aren't needed

## Did you add documentation?

- [ ] 📜 readme.md
- [ ] 📜 contributing.md
- [ ] 📜 wiki entry
- [ ] 🙋 I'd like someone to help write documentation, and will file a new issue for it
- [ ] 🙅 no documentation needed
