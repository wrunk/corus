# Corus - Addon Package for use with App Engine (Python)

"the spirit of surfeit"

## What is this (and what isn't this)?
- Appengine python admin website tools (name?)
- admin
- gae starting place
- Content, email and site management
- Appengine Specific
- Python
- Nudge 
    - can't use django because it won't play nice with another django app on the same gae module
    - Also want to keep this app VERY simple and self-contained.
- (maybe) Angular

## What to do now?
- MAKE ONE PAGE THAT POSTS SOME JSON DATA TO AND FROM PAGE DYNAMICALLY!
- Port all code from old sys


## Sections of Corus
- Email MGMT:
    - Very basic CMS (just paste HTML and text) (use the files section to upload assets for use in email)
    - Campaign mgmt
        - Split test several templates per campaign (maybe limit to 5 for now for sanity reasons)
        - Upload a csv of contacts
        - Select a campaign
        - View results
        - Get sum purty charts!!
    - (later feature) individual link tracking
    - Email campaigns need to be callable programatically (aka welcome/reg email can go out using campaign if set up)
- Basic Files (goes to brob store for now, should go to GCS later but thats a pain to set up)
    - Upload new file
    - List recent files
- Pages (console)
    - Add new page
    - Edit page
    - Delete page
    - Select template
    - Allow user to override template?
- Users
    - VERY simple
    - Admins
    - Regular users (content editors etc)
    - CANNOT rely on appengine admin system
