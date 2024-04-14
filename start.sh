#!/bin/bash

banner() {
    msg="# $* #"
    edge=$(echo "$msg" | sed 's/./#/g')
    echo "$edge"
    echo "$msg"
    echo "$edge"
}

banner "Building docker images"
docker compose build

banner "Starting services in the background"
docker compose up -d

banner "Waiting for all the services to come up, sleeping 15 seconds"
sleep 15

banner "Performing database migrations"
docker compose exec log_ingestor python manage.py migrate

banner "Creating admin user"
docker compose exec log_ingestor python manage.py createsuperuser --noinput 

printf "\n***********************************************************\n\n"
echo "Log Query dashboard should be up on http://localhost:8080"
echo "Log ingestor backend should be up on http://localhost:3000"
printf "\n***********************************************************\n"
