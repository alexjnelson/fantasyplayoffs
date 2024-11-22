# Base image for PostgreSQL
FROM postgres:latest

# Set up PostgreSQL environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase

# Copy the PostgreSQL initialization script
COPY init /docker-entrypoint-initdb.d/

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python for FastAPI
RUN apt-get update && apt-get install -y python3 python3-pip

# Install required tools for virtual environments
RUN apt-get update && apt-get install -y python3-venv

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment and install dependencies
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set the virtual environment as the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory for FastAPI
WORKDIR /app

# Copy FastAPI app and dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app ./app

# Expose ports for PostgreSQL and FastAPI
EXPOSE 5432 8000

# Run both PostgreSQL and FastAPI using a script
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
