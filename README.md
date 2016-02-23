# Picha a Django photo editing application.

Picha is an application created by Django and AngularJs, it allows a user upload a photo and apply effects, rotate, filters and write text on the photo. A user can then share the image to his facebook wall or save the new image with effects. View the [live demo]()  of the application.

###Installation
1. ######Requirements
 Ensure that python is installed on your machine, if not follow the link [Installing python](https://www.python.org/downloads/).
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
3. ######Cloning the repo

 To clone the repo type the following command in terminal:
 
 ```
 $ git clone git@github.com:andela-engmkwalusimbi/Picha.git
 ```
 
 To install all app requirements type these command in your terminal one after the other:
 
 ```
 $ cd Picha
 $ pip install -r requirements.txt
 ```
 
4. ######Setting up enviroment variables
 To set up enviroment variables follow the [Setting env variables](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps), as they will be used with the app.
 Ensure your create `DATABASE_URL`, `SECRET`, `FACEBOOK_SECRET` and `FACEBOOK_KEY` in your env variables.

5. ######Managing Database set up
To get started install Postgres on your local computer if you don’t have it already. if you haven't follow this [Setting up postgresql](http://www.postgresql.org/download/) and choose your appropriate OS.
Run the following commands on the terminal to set up tables and manage upgrades to tables if you change your models.


 * To create migrations, run the `migrate` command:

 ```
 $ python manage.py migrate
 ```

Your database is now ready to use with the app.

###Running the APP

To run the `APP` type the following command in your terminal:

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


###Running tests

To run tests type the following command in terminal:

```
$ python manage.py test
```



