# Corus - Addon Package for use with App Engine (Python)

"the spirit of surfeit"

## Set up process
- Please keep in mind these instructions are for starting a NEW project only. If you want to 
  integrate with an existing project please see below
- Clone this repo and git fetch && git checkout <current_version_#>
- This will ensure you are using a stable, production version as I will not update the version file
  or create a new version branch until it is tested and ready.
- ** master branch is my development branch and not considered stable
- Symlink Corus/corus into your project
- Run python -m init.py (TODO fix this) (this will safely initialize a new corus, app engine project
  for you
- Use Corus' run.sh to run your dev_appserver or just use it as you would like per normal
- Access Corus console via http://localhost:<your_port#>/
- This page will give you full instructions on getting the most of your new site including how to
  access the console
- Enjoy


## Integrating Corus with an existing App Engine project
- Follow all the above instructions except init.py
- You need to carefully audit my app.yaml and merge the required items into your app.yaml

## Ideal Set Up Process (NOT CURRENTLY AVAILABLE)
- Make a new virtualenv for your new App Engine project and activate it
- pip install corus
- python -m corus.set_up_here (app.yaml, index, queues, etc, lib/corusshit, main, run, deploy)
  this is inspired by python -m simplejson.tool
- run like above

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
- Name all things consistently (emails, etc)
- Port all code from old sys
- New a new ID structure
- MAKE ONE PAGE THAT POSTS SOME JSON DATA TO AND FROM PAGE DYNAMICALLY!
- Consider being able to make console pages for personal help (like html/css help) since each person
  will find different sites more or less helpful


## Sections of Corus
- Console Overview:
    - Initialize first load:
        - Load a starting page
        - Load a starting email
- Email MGMT:
    - Very basic CMS (just paste HTML and text) (use the files section to upload assets for use in 
      email)
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
    - CANNOT rely on appengine admin system via app.yaml
