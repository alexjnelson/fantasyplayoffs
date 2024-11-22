## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

---

### Step 2: Configure Environment Variables

1. Create a `.env` file in the root directory.
2. Copy the contents of `.env.example` into `.env`:
   ```bash
   cp .env.example .env
   ```
3. Update the values in `.env` as needed:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=mypassword
   POSTGRES_DB=mydatabase
   POSTGRES_PORT=5432
   ```

---

### Step 3: Build and Start the Database

Run the following command to build and start the PostgreSQL container:

```bash
docker-compose up --build
```

This will:

- Build the Docker image.
- Start the PostgreSQL container.
- Initialize the database with the schema and mock data.

---

### Step 4: Connect to the Database

You can connect to the PostgreSQL database using any client:

#### Connection Details

| **Parameter** | **Value**    |
| ------------- | ------------ |
| Host          | `localhost`  |
| Port          | `5432`       |
| Database Name | `mydatabase` |
| Username      | `postgres`   |
| Password      | `mypassword` |

#### Example Using `psql`:

```bash
psql -h localhost -U postgres -d mydatabase
```

#### Example Connection String:

```plaintext
postgresql://postgres:mypassword@localhost:5432/mydatabase
```

#### Example Using DBVisualizer or pgAdmin:

- Host: `localhost`
- Port: `5432`
- Database: `mydatabase`
- Username: `postgres`
- Password: `mypassword`

---

### Step 5: Stop the Database

To stop the container, press `CTRL+C` or run:

```bash
docker-compose down
```

---

### Step 6: Cleanup

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

## Troubleshooting

1. **Connection Refused:**

   - Ensure the container is running:
     ```bash
     docker ps
     ```
   - Confirm the port is correctly exposed:
     ```bash
     docker inspect postgres_container | grep HostPort
     ```

2. **Role Does Not Exist:**

   - Verify the `POSTGRES_USER` in your `.env` file matches the username you’re using to connect.
   - Rebuild the container with:
     ```bash
     docker-compose down --volumes
     docker-compose up --build
     ```

3. **Firewall Blocking Connection:**
   - Allow port `5432` through the firewall:
     ```bash
     sudo ufw allow 5432
     ```

---

## Customization

- Modify `init/schema.sql` to define your database schema.
- Modify `init/seed.sql` to preload custom mock data.

After making changes, rebuild the container:

```bash
docker-compose down --volumes
docker-compose up --build
```

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
