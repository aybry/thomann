# Thomann
A Django website for the translation workflow at Thomann. 

Comprises at the moment one tool:

## The Lookup Hub
A robust but lightweight custom categorised dictionary tool. 

A fully functional version (albeit without the dictionary itself) is available at https://lookup.ay-bryson.com/dictionary/sandbox. See the "Guide" page for how to use it.

# Deployment
A few notes on how to deploy the repo.

## Environment Variables 
The project requires a `.env` file in the top-level directory containing the following variables:

```
THOMANN_SECRET_KEY=   # Secret key for Django website
DBHOST=               # Hostname / IP address of (Postgres) DB
DBPORT=               # Port of DB
DBNAME=               # Name of DB
DBSCHEMA=             # Schema within DB
DBUNAME=              # Username with access to DB
DBPASS=               # Password for username
```

## Certbot
SSL certificates are supplied by Let's Encrypt. See the following repo (and the article linked within it) on how to get it up and running.
https://github.com/wmnnd/nginx-certbot

## Docker
You will require Docker on your machine as well as docker-compose.

## Start
Start the repo with the usual:

```
docker-compose up -d 
```
