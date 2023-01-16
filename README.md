# API of project "YaMDb".
![yamdb workflow](https://github.com/NotMainCode/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
## Description

The YaMDb project collects user feedback on creations (Title).
The creations are divided into categories: "Books", "Films", "Music", etc.
The list of categories can be expanded by the administrator.

In each category there is information about the creations.
The creations themselves are not stored in YaMDb;
you cannot watch a movie or listen to music here.

A creation can be assigned a genre from the preset list.
New genres can only be created by the administrator.

Users can leave text reviews for creations
and rate the creation in the range from one to ten (an integer);
from user ratings, an average rating of the creation is formed - rating (integer).
A user can leave only one review per creation.
###
Full API documentation is available at endpoint: ```redoc/```

## Examples of requests

- user registration *(POST)*
>api/v1/auth/signup/ 
>```
>{
>    "username": "my_username",
>    "email": "my_email"
>}
>```

- getting access JWT-token *(POST)*
>api/v1/auth/token/ 
>```
>{
>    "username": "my_username",
>    "confirmation_code": "my_confirmation_code"
>}
>```

## CI/CD based on GitHub Actions.

GitHub Actions workflow jobs:
- tests - functional tests, flake8 tests;
- build_and_push_to_docker_hub - create and push the application image to the DockerHub repository
- deploy - download images of Django application, postgres and nginx
  from the DockerHub repository to a remote server. Creation and start containers.
  Django app: collectstatic, migrate.

GitHub Actions workflow will start after pushing to the master branch.

## Technology

Python 3.7

Django 2.2.28

Django REST framework 3.12.4

Simple JWT 5.2.1

Docker 20.10.22

Docker Compose 2.14.2

PostgreSQL 13.0-alpine

GitHub Actions

## CI/CD setup.

- Create secret repository variables ([documentation](https://docs.github.com/en/actions/learn-github-actions/variables#creating-configuration-variables-for-an-environment)).
```
DB_ENGINE=django.db.backends.postgresql # indicate that we are working with postgresql
POSTGRES_DB=postgres # database name
POSTGRES_USER=postgres # login to connect to the database
POSTGRES_PASSWORD=postgres # database connection password
DB_HOST=db # name of the service (container)
DB_PORT=5432 # port for connecting to the database

DJANGO_SECRET_KEY=<Django_secret_key>

DOCKER_USERNAME=<docker_username>
DOCKER_PASSWORD=<docker_password>
DOCKER_REPO=<docker_username>/<image name>

SERVER_HOST=<server_pub_ip>
SERVER_PASSPHRASE=<server_passphrase>
SERVER_USER=<username>

SSH_KEY=<private key from a computer that has access to the server> # command to receive: cat ~/.ssh/id_rsa

TELEGRAM_TO=<telegram_account_ID> # https://telegram.im/@userinfobot?lang=en
TELEGRAM_TOKEN=<telegram_bot_token> # https://t.me/botfather
```

- Specify the public IP address of the server in the *docker-compose.yaml* and *nginx/default.conf* files.
```
...test: [ "CMD", "curl", "-f", "http://<server_pub_ip>/admin" ]...
```
```
...server_name <server_pub_ip>;...
```

- Copy *docker-compose.yaml*, *deploy_job.sh* files and *nginx* folder to the server.
```
scp <path_to_file>/docker-compose.yaml <username>@<server_pub_ip>:/home/<username>
scp <path_to_file>/deploy_job.sh <username>@<server_pub_ip>:/home/<username>
scp -r <path_to_folder>/nginx <username>@<server_pub_ip>:/home/<username>
```

- Connect to the server.
```
ssh <username>@<server_pub_ip>
```

Install [docker](https://docs.docker.com/engine/install/ubuntu/)
and [compose plugin](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).
Follow the [steps after installing Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/).
###
After the successful completion of the GitHub Actions workflow,
the project is available at: ```http://<server_pub_ip>/admin/```.
###

- Create superuser
```
docker compose exec web python manage.py createsuperuser
```

- Enter test data into the database
```
docker compose exec web python manage.py loaddata db_fixtures.json
```

- Create a database dump
```
sudo docker compose exec web python manage.py dumpdata > db_dump.json
```

## Authors

[NotMainCode](https://github.com/NotMainCode)

[Vas1l1y](https://github.com/Vas1l1y)

[SerMikh1981](https://github.com/SerMikh1981)

###
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
