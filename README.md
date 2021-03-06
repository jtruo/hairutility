# hairutility-web

HairUtility is a side project website I made to help people get better haircuts. In order to help people receive better haircuts, I created hair profiles to store more information about haircuts onto the website/apps. The UI/UX design was based off of a bootstrap template that I modified.

The greatest obstacle was the differenting hair types/shapes that make it difficult to replicate another person's haircut. There is hardly any documentation on the code which is bad practice. I invested most of my time rapidly developing the full-stack django website and doing customer interviews.

After interviewing ~60 students at Alpha Chi Omega at Purdue, I decided to shelve the project because I lost interest in haircuts and the app would only be helpful to a small niche of people.

I attempted tried to implement some unit-tests, but I ended up disabling the tests so that I could develop faster. I used a hobby/qa server on Heroku to test my implementations on the webserver. 

https://www.hairutility.com/

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Uploading/Retrieving Images at Scale

Image Implementation:
Uploading images are based off of a common practice. Images are uploaded from the users's phones into an AWS S3 bucket. The path to the image is stored in the Django/Heroku PostgreSQL database instead of the full link to the S3 bucket. This saves a small chunk of space with the image sizing. When retrieving images, users don't download and store the images directly. The database keeps track of what images users have "Liked" and retrieves them quickly. CloudFront capability could be added to improve image loading times/caching. 

# Local Development

Start the dev server for local development:

docker-compose up

When adding new static files to the folder;

docker-compose build 


Run a command inside the docker container:

docker-compose run --rm web [command]


Do this everytime you make changes to the database/models.py:

If unable to migrate due to missing column or etc., make sure all references to old models in views.py/admin.py are commented out or name changed as well

docker-compose run --rm web python3 manage.py makemigrations
docker-compose run --rm web python3 manage.py migrate

Delete all docker containers

docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

Remove postgres container
docker rmi postgres:10

AWS S3 Local + Online

ENV vars for Local. Local dev must provide a .env file with AWS keys and S3 for local dev

# Known Issues

If there is no hair profile image in AWS3 for single-hair-profile but the image key is in db, the website will crash

# Personal Notes

AWS ECS

View push commands in repo
Run task

Initialize the production server:


heroku create hairutility-prod --remote prod && \
    heroku addons:create newrelic:wayne --app hairutility-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app hairutility-prod && \
    heroku config:set SECRET_KEY=`openssl rand -base64 32` \
        AWS_ACCESS_KEY_ID="Add your id" \
        AWS_SECRET_ACCESS_KEY="Add your key" \
        AWS_STORAGE_BUCKET_NAME="hairutility-prod" \
        CONFIGURATION="Production" \
        SETTINGS_MODULE="hairutility.config" \
        --app hairutility-prod


Initialize the qa server:

heroku create hairutility-qa --remote qa && \
    heroku addons:create newrelic:wayne --app hairutility-qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app hairutility-qa && \
    heroku config:set SECRET_KEY=`openssl rand -base64 32` \
        AWS_ACCESS_KEY_ID="Add your id" \
        AWS_SECRET_ACCESS_KEY="Add your key" \
        AWS_STORAGE_BUCKET_NAME="hairutility-qa" \
        CONFIGURATION="Production" \
        SETTINGS_MODULE="hairutility.config" \
        --app hairutility-qa



Commit your changes and push to master and qa to trigger your first deploys:

Step 1:

git push origin master:qa && \
git push origin master

Step: 2
heroku container:login && \
heroku container:push web && \
heroku container:release web --app hairutility-qa

To make database migrations (almost everytime you change your model):

heroku run bash
./manage.py migrate

Run the django shell
docker-compose run --rm web python3 manage.py shell

Port already allocated error = restart docker application

PostgreSQL/RDS

Connect by:

