# Items List

## Description
Sample Wed app using postgresql and docker

## To run
git clone https://github.com/TsvetoslavM/VOT-Tues.git
cd VOT-Tues

Create a .env file in the root directory and add the following environment variables:

POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=db_name

Build and run the Docker containers:
docker-compose up --build

Access the application at http://localhost:5000.
