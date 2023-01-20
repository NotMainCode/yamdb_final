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
Full API documentation is available at endpoint: ```redoc/``` ([temporary URL](http://51.250.25.37/admin))

## Examples of requests

- user registration *(POST)*
>api/v1/auth/signup/ 
>```json
>{
>    "username": "my_username",
>    "email": "my_email"
>}
>```

- getting access JWT-token *(POST)*
>api/v1/auth/token/ 
>```json
>{
>    "username": "my_username",
>    "confirmation_code": "my_confirmation_code"
>}
>```

## Triggers of GitHub Actions workflow
- ```push to any branch``` - run flake8 and functional tests
- ```push to master branch``` - push the app image to the DockerHub repository, 
run project on remote server, Django app: collectstatic, migrate

## Technology

Python 3.7

Django 2.2.28

Django REST framework 3.12.4

Simple JWT 5.2.1

Docker 20.10.22

Docker Compose 2.14.2

PostgreSQL 13.0-alpine

Nginx 1.21.3-alpine

GitHub Actions

## Launch

- Create secret repository variables ([documentation](https://docs.github.com/en/actions/learn-github-actions/variables#creating-configuration-variables-for-an-environment)).
```
DOCKER_USERNAME=<docker_username>
DOCKER_PASSWORD=<docker_password>
DOCKER_REPO=<docker_username>/<image name>
SERVER_HOST=<server_pub_ip>
SERVER_PASSPHRASE=<server_passphrase>
SERVER_USER=<username>
SSH_KEY=<--BEGIN OPENSSH PRIVATE KEY--...--END OPENSSH PRIVATE KEY--> # cat ~/.ssh/id_rsa
TELEGRAM_TO=<telegram_account_ID> # https://telegram.im/@userinfobot?lang=en
TELEGRAM_TOKEN=<telegram_bot_token> # https://t.me/botfather


- ENV_FILE variable value

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=<database name>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password> 
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=<Django_secret_key>
DOCKER_REPO=<docker_username>/<image name>
SERVER_HOST=<server_pub_ip>
SERVER_URL=http://<server_pub_ip>/admin
```


- Copy *docker-compose.yaml* file and *nginx* folder to the server.
```shell
scp <path_to_file>/docker-compose.yaml <username>@<server_pub_ip>:/home/<username>
scp -r <path_to_folder>/nginx <username>@<server_pub_ip>:/home/<username>
```

- Connect to the server.
```shell
ssh <username>@<server_pub_ip>
```

Install [docker](https://docs.docker.com/engine/install/ubuntu/)
and [compose plugin](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).
Follow the [steps after installing Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/).
###

After activation and successful completion of the GitHub Actions workflow,
the project is available at: ```http://<server_pub_ip>/admin/```

###

- Create superuser
```shell
docker compose exec web python manage.py createsuperuser
```

- Enter test data into the database
```shell
docker compose exec web python manage.py loaddata db_fixtures.json
```

- Create a database dump
```shell
sudo docker compose exec web python manage.py dumpdata > db_dump.json
```

## Authors

[NotMainCode](https://github.com/NotMainCode)

[Vas1l1y](https://github.com/Vas1l1y)

[SerMikh1981](https://github.com/SerMikh1981)

###
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
