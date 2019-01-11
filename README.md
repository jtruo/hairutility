# hairutility-web

[![Build Status](https://travis-ci.org/jtruo/hairutility-web.svg?branch=master)](https://travis-ci.org/jtruo/hairutility-web)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Django api and web. Check out the project's [documentation](http://jtruo.github.io/hairutility-web/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Local Development

Start the dev server for local development:

docker-compose up

Run a command inside the docker container:

docker-compose run --rm web [command]


Do this everytime you make changes to the database/models.py:

docker-compose run --rm web python3 manage.py makemigrations
docker-compose run --rm web python3 manage.py migrate

Delete all docker containers

docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

Remove postgres container
docker rmi postgres:10


# Continuous Deployment

Deployment is automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Follow these steps to enable this feature.


AWS ECS

View push commands in repo
Run task




Initialize the production server:


heroku create hairutility-prod --remote prod && \
    heroku addons:create newrelic:wayne --app hairutility-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app hairutility-prod && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="hairutility-images-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="hairutility.config" \
        --app hairutility-prod


Initialize the qa server:


heroku create hairutility-qa --remote qa && \
    heroku addons:create newrelic:wayne --app hairutility-qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app hairutility-qa && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="hairutility-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="hairutility.config" \
        --app hairutility-qa


Securely add your Heroku credentials to Travis so that it can automatically deploy your changes:


travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add


Commit your changes and push to master and qa to trigger your first deploys:

Step 1:

git commit -a -m "ci(travis): add Heroku credentials" && \
git push origin master:qa && \
git push origin master

Step: 2
heroku container:login
heroku container:push web
heroku container:release web --app hairutility-qa

To make database migrations (almost everytime you change your model):

heroku run bash
./manage.py migrate

Run the django shell
docker-compose run --rm web python3 manage.py shell

Port already allocated error = restart docker application