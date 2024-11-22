FROM postgres:latest


# Copy initialization scripts to the Docker entrypoint
COPY init /docker-entrypoint-initdb.d/

# Expose the default PostgreSQL port
EXPOSE 5432