# ProjectForum Overview

This is a project for CS 169 at UC Berkeley. We are creating a website that will
allow people to post jobs and collaborate to get things done.

# Setting up ProjectForum

## Setting up the local database

Make sure you have postgress running and then run the following command to
create the database.

```
psql -c "CREATE DATABASE projectforum_db"
```

Then fill in the structure of the database with the following command:
```
python manage.py migrate
```

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
scss, then you need to set up Sass.

[Koala](http://koala-app.com/) is the tool we used to compile the Scss files. It
is a cross platform compiler that allows autoprefixing. This means that it adds
the appropriate vendor prefixes to the CSS rules to have better compatibility.

## Other requirements

ProjectForum requires the python modules Whitenoise and Requests to run. Just
pip install them to get it working.

# Running ProjectForum

ProjectForum is set up to deploy to Heroku. Just deploy and then run the
following command to set up the databases.

```
$ heroku run python manage.py migrate
```

**If you run into migration issues**, you can empty the database from the heroku
[portal](https://dashboard.heroku.com/apps) and then run

```
heroku run python manage.py syncdb
````

# Running the Tests

ProjectForum requires the python module mock to run. Just pip install it to get
it working.

## Running Locally

1. Comment out the lines for `TEST_DATABASES` and `TEST_RUNNER` in `settings.py`

1. Run the following command:

```
$ python manage.py test
```

## Running Remotely

To run the tests on Heroku, first make a new free postgres database on Heroku
using the [portal](https://dashboard.heroku.com/apps). Then you should be able
to see what the url to the value of the config variable
HEROKU_POSTGRESQL_\<COLOR>_URL. Use the following command to see the value.

```
$ heroku config --app *app name*
```

Then use this command to set the value

```
$ heroku config:set TEST_DATABASE_URL=*postgres database url* --app *app name*
```

Finally run this command to run the tests.

```
$ heroku run python manage.py test --app *app name*
```

## Test Coverage

To get a report on test coverage, you can run the following command:

```
heroku run "coverage run --source='./projectforum/' manage.py test; coverage report" --app *app name*
```

## Pull-Request Checklist:
* Add tests for at least the main functionality of your code. This way if you or
someone else accidentaly breaks your code, they will know.
* Run the tests, make sure they all pass.
* push your feature branch to the git repo `git push origin \<feature_branch>`
* make a pull request on git hub with a description of what your feature does
