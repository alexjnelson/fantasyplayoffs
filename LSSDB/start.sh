#!/bin/bash

# Start PostgreSQL in the background
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
until pg_isready -h localhost -p 5432; do
  sleep 1
done

# Start FastAPI
echo "Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
