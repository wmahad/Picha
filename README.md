# Picha: a Django photo editing application. [![Build Status](https://travis-ci.org/andela-engmkwalusimbi/Picha.svg?branch=develop)](https://travis-ci.org/andela-engmkwalusimbi/Picha) [![Coverage Status](https://coveralls.io/repos/github/andela-engmkwalusimbi/Picha/badge.svg?branch=develop)](https://coveralls.io/github/andela-engmkwalusimbi/Picha?branch=develop) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/a57180184fe445b982f1097b4b970bcb/snapshot/origin:develop:HEAD/badge.svg)](https://www.quantifiedcode.com/app/project/a57180184fe445b982f1097b4b970bcb?branch=origin%2Fdevelop)

Picha is a Django and AngularJs application, that allows a user upload a photo and apply effects, rotate, filters and write text on the photo. A user can then share the image to his Facebook wall or save the new image with effects. View the [live demo](https://pichaa.herokuapp.com/)  of the application.

###Installation
1. ######Requirements
 Ensure that python is installed on your machine, if not follow the link [Installing Python](https://www.python.org/downloads/).
 * [Python 2.7+](https://www.python.org/) 
 * [Django](https://www.djangoproject.com/)
 * [Django REST framework](http://www.django-rest-framework.org/)
 * [AngularJS](https://angularjs.org/)
 * [Facebook Javascript SDK](https://developers.facebook.com/docs/javascript)
 * [Pillow](http://pillow.readthedocs.org/)
 * Among others as listed in `requirements.txt`
 
2. ######Installing virtualenvwrapper
 A Virtual Environment is a tool to keep the dependencies required by different projects in separate directories on a computer.
 To install virtualenvwrapper follow the link [installing virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
3. ######Cloning the Repository

 To clone the repo type the following command in terminal:
 
 ```
 $ git clone git@github.com:andela-engmkwalusimbi/Picha.git
 ```
 
 To install all app requirements type these command in your terminal one after the other:
 
 ```
 $ pip install -r requirements.txt
 ```
 
4. ######Setting Enviroment Variables
 To setup enviroment variables follow the [env-variable setup tutorial](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps), as they will be used with the app.
 Ensure your create `DATABASE_URL`, `SECRET`, `FACEBOOK_SECRET` and `FACEBOOK_KEY` in your env variables.

5. ######Managing Database Setup
To get started install Postgres on your local computer if you don’t have it already installed. if you haven't follow this [configuring PostgreSQL](http://www.postgresql.org/download/) and choose your appropriate OS.
Run the following commands on the terminal to set up tables and manage upgrades to tables if you change your models.


 * To create migrations, run the `migrate` command:

 ```
 $ python manage.py migrate
 ```

Your database is now ready to use with the app.

###Running the App

To run the `App` type the following command in your terminal:

```
$ python manage.py runserver
```

And the response on the terminal will look like:

```
System check identified no issues (0 silenced).
January 21, 2016 - 11:55:00
Django version 1.9, using settings 'picha.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

The default url is `http://127.0.0.1:8000/`. Use this in the browser of your choice.


###Running Tests

To run tests type the following command in terminal:

```
$ python manage.py test
```



