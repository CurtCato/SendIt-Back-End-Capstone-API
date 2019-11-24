###python-SendIt-api-template###

There are a couple steps to run this server. After you clone the repo, cd into it and perform the following steps:


In the root project directory run the command: python manage.py makemigrations Next run: python manage.py migrate

Run this command: python -m venv SendItAPI
Next, in cmd cd into the SendItEnv directory within the project directory
Then cd into the Scripts directory and run the command: Start activate.bat
In the root directory run the command: pip install django autopep8 pylint djangorestframework django-cors-headers pylint-django mapbox googlemaps
Run: pip freeze -r requirements.txt
The next steps are for setting up the database:

In the root project directory run the command: python manage.py makemigrations
Next run: python manage.py migrate


Now that your database is set up all you have to do is run the command:

python manage.py runserver

You can test your new server out in postman if you so desire.