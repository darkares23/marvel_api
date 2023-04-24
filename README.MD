# Marvel Impossible Travel Investigation

This Django project investigates an impossible travel alert triggered by Spectrum. It consumes the Marvel API to gather information about Spectrum and other characters she's worked with in comics, and stores the data in a PostgreSQL database. The project includes a Docker setup and an Nginx configuration for ease of deployment.

In this project, we use Celery to manage asynchronous tasks, which allows for better performance and responsiveness of the application.

The Marvel API has a rate limit of 3000 calls per day, and the data retrieval process involves multiple API calls to collect information about a character and their related characters. Performing these API calls synchronously would cause the application to stall and become unresponsive to user requests while waiting for the API responses.

By using Celery, we can offload these time-consuming tasks to background workers, allowing the application to continue processing other requests and providing a better user experience. Users can submit requests to fetch data from the Marvel API without having to wait for the results immediately, and the application remains responsive during the data retrieval process.

## Prerequisites

- Docker
- Docker Compose
- mkcert

## Setup
Install mkcert on your system. Please refer to the official documentation for installation instructions for your operating system.
- `sudo make create_certs` Is used to generate local certs for using ssl request locally, You need to install mkcert in order to run this command
- `make build`: Builds the Docker containers.
- `make superuser`: Creates a Django superuser allowed to access the admin panel where you can visualize all character data and images.
- `make up`: Starts dockers containers

In this project, we use docker-compose to manage multiple services, each responsible for a specific part of the application. The services included are:

- web: This service runs the Django web application using the Gunicorn WSGI server. It serves the web interface and handles incoming requests from users.

- db: This service runs a PostgreSQL database server, which is responsible for storing the application data. Django interacts with the database server to perform CRUD (Create, Read, Update, Delete) operations on the character data.

- redis: This service runs a Redis server, which is an in-memory data structure store that can be used as a message broker for Celery. It helps manage the communication between the main application and the Celery workers.

- celery: This service runs Celery workers that execute asynchronous tasks, such as fetching data from the Marvel API. These workers process tasks in the background, allowing the main application to remain responsive while handling time-consuming operations.

- nginx: This service runs an Nginx web server, which acts as a reverse proxy for the Django web application. Nginx is responsible for handling incoming requests, serving static files, and forwarding requests to the Django application. It can also provide SSL termination for secure HTTPS connections.

## Usage

The project provides the following endpoints:

- `/investigation/populate/`: Populates the database with Spectrum and related characters using the Marvel API.
- `/investigation/characters/`: Retrieves a list of all characters stored in the database.
- `/investigation/export_csv/`: Creates a CSV file with all the characters data stored in the database
- `/investigation/characters/<int:character_id>/`: Retrieves a specific character by ID.
- `/investigation/characters/<str:name>/delete/`: Deletes a character by name.

You can access the Django admin panel at `/admin/`.

## Nginx Configuration

The project includes a basic Nginx configuration file located at `./nginx/default.conf`. The Nginx container is set up to serve the Django application using the `uwsgi` protocol. To customize the Nginx configuration, modify the `default.conf` file as needed.

This project includes a local SSL/TLS certificate generation using mkcert to enable secure HTTPS connections during development. Mkcert is a simple tool for creating locally-trusted certificates that are recognized by your system and browsers, allowing you to develop and test your application with HTTPS locally.

To set up a local certificate using mkcert, follow these steps:

Install mkcert on your system. Please refer to the official documentation for installation instructions for your operating system.

## Makefile Commands

- `make build`: Builds the Docker containers.
- `make up`: Starts the Docker containers.
- `make down`: Stops the Docker containers.
- `make makemigrations`: Creates the Django migrations files.
- `make migrate`: Applies the Django migrations.
- `make superuser`: Creates a Django superuser allowed to access the admin panel where you can visualize all character data and images.
- `make test`: Runs the Django test suite.

