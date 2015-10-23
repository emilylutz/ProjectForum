#Running Code and things to remember before you run locally.

We are using:
- Mailgun for all of our email needs
- Sass for CSS
- Selenium for testing
- Whitenoise
- Requests

# Setting up Mailgun

Make sure you have these set up before proceeding.

`python manage.py migrate`
`heroku local` to simulate a local server

#Compiling Sass to generate the CSS

We will be using Sass for all of our CSS needs.

compile_scss.sh will run a script (assuming you set it up using ruby) that will automatically update the css files as you make changes to sass.

