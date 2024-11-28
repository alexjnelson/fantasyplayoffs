# **Quickstart Guide**

### **Prerequisites**
- Install [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install).
- Ensure Python (>=3.9) and Node.js (>=14) are installed on your machine.

---

### **1. Clone the Repository**
```bash
git clone git@github.com:alexjnelson/fantasyplayoffs.git
cd fantasyplayoffs
```

---

### **2. Setup Environment Variables**
Copy the `.env` files to their respective directories (`app/.env`, `LSSDB/.env`, and `frontend/.env`) based on the configuration below:

- **`app/.env`:**
  ```plaintext
  ENVIRONMENT=dev
  DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/mydatabase
  ALLOW_ORIGINS=["http://localhost:3000","http://localhost:8080"]
  ```

- **`LSSDB/.env`:**
  ```plaintext
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=mypassword
  POSTGRES_DB=mydatabase
  POSTGRES_PORT=5432
  ```

- **`frontend/.env`:**
  ```plaintext
  REACT_APP_ENVIRONMENT=dev
  REACT_APP_BASE_URL=http://localhost:3000
  ```

---

### **3. Start the LSSDB**
From the `LSSDB` directory:
```bash
docker-compose up --build
```
This starts the PostgreSQL database and the mock Live Scoring Service.

---

### **4. Start the Backend**
1. Navigate to the `app` directory:
   ```bash
   cd app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Use .venv\Scripts\activate on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be accessible at `http://localhost:8000/` with API documentation at `http://localhost:8000/docs`.

---

### **5. Start the Frontend**
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install the dependencies:
   ```bash
   npm i
   ```

3. Start the frontend:
   ```bash
   npm start
   ```

The app will open in your browser at `http://localhost:3000`.

---

### **Stopping the Services**
- **LSSDB:** `docker-compose down` (run in the `LSSDB` directory).
- **Backend:** Press `CTRL+C` in the terminal running `uvicorn`.
- **Frontend:** Press `CTRL+C` in the terminal running `npm start`.

---

# Full Setup Guide

## Prerequisites

- Install [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install).
- Ensure Python (>=3.9) and Node.js (>=14) are installed on your machine.

## Environment setup

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
- Start the mock Live Scoring Service.
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

#### Accessing the Database from Another Application

If another application (such as the `app` backend) needs to connect to this database, configure its `.env` file with the following connection string:

```
DATABASE_URL = "postgresql://postgres:mypassword@localhost:5432/mydatabase"
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

## Starting the main app

### Create a virtual environment

This will ensure the project requirements don't conflict with any Python packages you have installed on your machine. 

Run the following command in the `app` directory:

```bash
python -m venv .venv
```

---

### Install the requirements

Ensure your virtual environment is activated:

```bash
./.venv/bin/activate
```

---

### Start the backend

Start the FastAPI app in reload mode. As you modify the code, your changes will be reflected in the FastAPI live.

```bash
uvicorn main:app --reload
```

---

### Connect to the backend

The backend will be accessible at:

```
http://localhost:8000/
```

You can also view the available endpoints at:

```
http://localhost:8000/docs
```

This provides an interactive UI to test the API. Any new endpoints created will be automatically included here.

---

### Stopping the backend

To stop the app, press `CTRL+C`. No cleanup required.

---

## Starting the frontend

### Install the node modules

From the `frontend` directory, run the command:

```bash
npm i
```

---

### Start the frontend

To start the frontend:

```bash
npm start
```

---

### View the app

The previous step should open the frontend in a new tab. In general, you can view the app at:

```
http://localhost:3000
```

---

### Stopping the frontend

To stop the app, press `CTRL+C`. No cleanup required.

---

# License

This project is licensed under the MIT License. See `LICENSE` for details.
