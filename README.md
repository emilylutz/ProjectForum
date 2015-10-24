# ProjectForum Overview

This is a project for CS 169 at UC Berkeley. We are creating a website that will
allow people to post jobs and collaborate to get things done.

# Setting up ProjectForum

## Setting up Mailgun

ProjectForum uses [Mailgun](https://mailgun.com) to send emails. To get this
working, you need to make an account, and take the API key and server name to
set two environmment variables. The API key would start with 'key-'. The domain
could, for example, start with 'sandbox' and end with '.mailgun.org'

```
$ heroku config:set MAILGUN_ACCESS_KEY=*API Key Here*
$ heroku config:set MAILGUN_SERVER_NAME=*Domain here*
```

## Setting up Sass

ProjectForum uses [Sass](http://sass-lang.com/) as a CSS precompiler. The css
files are already compiled in the repository, but if you want to change the
scss, then you need to set up Sass. There is a script, `compile_scss.sh`, in the
root directory that will automatically update the css files as you make changes
to the scss. However it requires ruby installed with the Sass gem.

## Other requirements

ProjectForum requires the python modules Whitenoise and Requests to run. Just
pip install them to get it working.

# Running ProjectForum

ProjectForum is set up to deploy to Heroku. Just deploy and then run the
following command to set up the databases.

```
$ heroku run python manage.py migrate
```

# Running the Tests

Set up ProjectForum to run locally and then run the following command:

```
$ python manage.py test
```
