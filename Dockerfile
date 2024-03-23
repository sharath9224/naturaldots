# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI application code into the container
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=Sharath@9224
ENV POSTGRES_DB=Sharath

# Install PostgreSQL and configure the database
RUN apt-get update && apt-get install -y postgresql
RUN service postgresql start && \
    su postgres -c "psql -c \"CREATE DATABASE mydatabase;\"" && \
    su postgres -c "psql -c \"CREATE USER myuser WITH PASSWORD 'mypassword';\"" && \
    su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;\""

# Expose port for FastAPI application
EXPOSE 8000

# Run FastAPI application and PostgreSQL database when the container launches
CMD service postgresql start && uvicorn main:app --host 0.0.0.0 --port 8000
