The Fantasy Playoff Challenge

# Quickstart

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Setup

### Clone the repository

Run the following command where you want to clone the repository:

```bash
git clone git@github.com:alexjnelson/fantasyplayoffs.git
```

You will see three directories - `app`, `frontend`, and `LSSDB`.

#### Main App

The `app` directory contains the main backend, a FastAPI app. The app is broken down into `routers`, `services`, and `models`. The routers define the endpoints that the frontend can query to run the fantasy app. The services handle the logic performed in the backend for these endpoints including database queries, which are made using the SQLAlchemy ORM. The models are the SQLModel definitions that validate the data being sent to and from the database, as well as the data passed throughout the app. Migrations on the database are managed using Alembic.

#### Frontend

The `frontend` directory contains a React app. It is broken down into `pages`, `components`, `services`, and `utils`. Each route will have a page, and reusable components on each page can be stored in the `components` directory. `services` contain the logic used to query the backend API with an axios instance. `utils` has several contexts, providers, and hooks used across the app, such as for authentication and sharing a preconfigured axios instance.

#### LSSDB

The `LSSDB` is the Live Scoring Service (LSS) and Database and contains mock versions of the services required for development. The production services for the hosted app will deployed in the cloud, though you can find the code for the production Live Scoring Service in this directory as well. Mock services are provided here for developmental efficiency; you will be able to run your own Postgres instance as defined by the docker image in the `LSSDB` folder, and you can simulate live games with the mock LSS even if no games are being played. Both the production and mock LSS connect to the main app via websocket so live data can be pushed as soon as it becomes available.

---

### Setup environment variables

Copy the .env files below to their respective locations:

#### app/.env

```
ENVIRONMENT=dev
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/mydatabase
ALLOW_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

#### LSSDB/.env

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
POSTGRES_PORT=5432
```

#### frontend/.env

```
REACT_APP_ENVIRONMENT=dev
REACT_APP_BASE_URL=http://localhost:3000
```

---
 
## Starting the LSSDB

### Build and Start the Database

Run the following command to build and start the PostgreSQL container and mock Live Scoring Service

```bash
docker-compose up --build
```

This will:

- Build the Docker image.
- Start the PostgreSQL container.
- Start the Live Scoring Service.
- Initialize the database with the schema and mock data.

---

### Connect to the Database

You can connect to the PostgreSQL database using any client:

#### Connection Details

| **Parameter** | **Value**    |
| ------------- | ------------ |
| Host          | `localhost`  |
| Port          | `5432`       |
| Database Name | `mydatabase` |
| Username      | `postgres`   |
| Password      | `mypassword` |

#### Example Connection String:

```plaintext
postgresql://postgres:mypassword@localhost:5432/mydatabase
```

---

### Stopping the Database

To stop the container, press `CTRL+C` or run:

```bash
docker-compose down
```

---

### Cleanup

If you want to remove all data and reset the database:

```bash
docker-compose down --volumes
docker-compose up --build
```

---

## Accessing the Database from Another Project

If another project needs to connect to this database, configure its `.env` file with the following connection string:

```
DATABASE_URL = "postgresql://postgres:mypassword@localhost:5432/mydatabase"

```

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
