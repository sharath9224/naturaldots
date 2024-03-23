Water Quality Observations Platform
This project aims to develop a Water Quality Observations Platform using FastAPI for managing records of water quality measurements from various locations. The platform supports CRUD operations for these records, as well as search functionality based on specific parameters.

Features
Create, Read, Update, and Delete operations for water quality observation records
Search functionality to query records by location, date range, and water quality parameters
Containerized using Docker for easy deployment and scalability
Deployed to a simulated AWS EC2 instance using LocalStack for testing and development
Requirements
To run the application locally, you will need:

Docker installed on your machine
LocalStack installed for simulating AWS services locally
Usage
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/your_username/water-quality-observations-platform.git
Navigate to the project directory:

bash
Copy code
cd water-quality-observations-platform
Build the Docker images:

Copy code
docker-compose build
Start the containers:

Copy code
docker-compose up
Access the FastAPI application at http://localhost:8000

Environment Variables
POSTGRES_USER: PostgreSQL username
POSTGRES_PASSWORD: PostgreSQL password
POSTGRES_DB: PostgreSQL database name
