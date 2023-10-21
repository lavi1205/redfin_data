# Redfin Data Project

**Author:** Thinh Pham

## Project Overview

This project automates the extraction, transformation, and loading (ETL) of real estate market data from the Redfin API into an Amazon S3 bucket. It utilizes Apache Airflow for orchestrating ETL tasks, and the DAG (Directed Acyclic Graph) within this project is responsible for performing the ETL operations.

## Setup and Requirements

Before running the Redfin Data project, ensure that you have the following dependencies and setup in place:

- Docker and Docker Compose for running Apache Airflow (version 2.7.1).
- AWS S3 buckets (`raw-bucket-123` and `final-bucket-123`) to store raw and processed data.

## Running Apache Airflow Using Docker Compose

### Setup Steps

1. **Clone the project repository to your local machine.**

2. **Navigate to the project directory.**

3. **Create a `.env` file in the project directory with the following environment variables:**

   ```env
   AIRFLOW_UID=1000
   AIRFLOW_GID=1000
   POSTGRES_USER=airflow
   POSTGRES_PASSWORD=airflow
   POSTGRES_DB=airflow
   
4. **Start Apache Airflow**
Open a terminal and navigate to the project directory.

Run the following command to start Apache Airflow using Docker Compose:
docker-compose up

Certainly! Here's your modified README with the "DAG Overview," "DAG Execution Flow," and "Conclusion" sections included, and formatted to be copyable:

markdown
Copy code
# Redfin Data Project

**Author:** Thinh Pham

## Project Overview

This project automates the extraction, transformation, and loading (ETL) of real estate market data from the Redfin API into an Amazon S3 bucket. It utilizes Apache Airflow for orchestrating ETL tasks, and the DAG (Directed Acyclic Graph) within this project is responsible for performing the ETL operations.

## Setup and Requirements

Before running the Redfin Data project, ensure that you have the following dependencies and setup in place:

- Docker and Docker Compose for running Apache Airflow (version 2.7.1).
- AWS S3 buckets (`raw-bucket-123` and `final-bucket-123`) to store raw and processed data.

## Running Apache Airflow Using Docker Compose

### Setup Steps

1. **Clone the project repository to your local machine.**

2. **Navigate to the project directory.**

3. **Create a `.env` file in the project directory with the following environment variables:**

   ```env
   AIRFLOW_UID=1000
   AIRFLOW_GID=1000
   POSTGRES_USER=airflow
   POSTGRES_PASSWORD=airflow
   POSTGRES_DB=airflow
Start Apache Airflow
Open a terminal and navigate to the project directory.

Run the following command to start Apache Airflow using Docker Compose:

bash
Copy code
docker-compose up
This will start the Airflow web server and scheduler.

