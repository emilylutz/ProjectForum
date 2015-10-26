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
following commands to set up the databases.

This will remove the current objects in the database. Not a good idea in
production, but while we are still in development it is fine and removes a lot
of headaches later with a bad migration.

```
$ heroku run python manage.py flush
```

This will update the database structure.
```
$ heroku run python manage.py migrate
```

# Running the Tests

Set up ProjectForum to run locally and then run the following command:

```
$ python manage.py test
```

To run the tests on Heroku, first make a new postgres database on Heroku. Then
you should be able to see what the url to the value of the config variable
HEROKU_POSTGRESQL_<COLOR>_URL. Use the following command to see the value.

```
$ heroku config
```

Then use this command to set the value

```
$ heroku config:set TEST_DATABASE_URL=*postgres database url*
```

Finally run this command to run the tests.

```
$ heroku run python manage.py test
```

## Pull-Request Checklist:
* Add tests for at least the main functionality of your code. This way if you or someone else accidentaly breaks your code, they will know.
* Run the tests, make sure they all pass.
* push your feature branch to the git repo `git push origin \<feature_branch>`
* make a pull request on git hub with a description of what your feature does
