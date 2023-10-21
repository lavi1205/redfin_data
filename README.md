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

Access the Airflow web UI by visiting http://localhost:8080 in your web browser.

DAG Overview
The project includes a single DAG, named redfin_analytics_dag. This DAG automates the ETL process for Redfin market data. Here's a detailed breakdown of the DAG tasks and their functionality:

START: A DummyOperator that serves as the initial task of the DAG.

check_api_status: A PythonOperator that checks the status of the Redfin API by making an HTTP request to the provided URL. If the API is responsive, it prints a success message; otherwise, it prints an error message.

task_extract_redfin_data: Another PythonOperator that extracts data from the Redfin API. It downloads the data, saves it as a CSV file with a timestamp, and returns the file name and timestamp as XCom values for later tasks.

upload_to_S3_raw_bucket: This PythonOperator uploads the raw data CSV file to the raw-bucket-123 S3 bucket. It uses the XCom values from the previous task for the file name.

task_transform_redfin_data: This PythonOperator reads the raw data CSV, performs data transformation (e.g., handling missing values, date parsing, and month name conversion), and saves the transformed data as a new CSV file. It returns the new file name.

upload_to_s3_final_data_bucket: Another PythonOperator that uploads the transformed data CSV file to the final-bucket-123 S3 bucket.

END: A DummyOperator representing the end of the DAG.

DAG Execution Flow
The execution flow of the DAG is as follows:

The DAG starts with the START task.

The check_api_status task checks the Redfin API's status.

The task_extract_redfin_data task extracts data and saves it as a raw data CSV.

The upload_to_S3_raw_bucket task uploads the raw data to the raw-bucket-123.

The task_transform_redfin_data task performs data transformation and saves the processed data as a new CSV.

The upload_to_s3_final_data_bucket task uploads the transformed data to the final-bucket-123.

Finally, the DAG ends with the END task.

This DAG ensures that the Redfin market data is fetched, transformed, and stored in the designated S3 buckets. You can schedule this DAG to run at specific intervals as needed.

Note: You must provide your AWS credentials and access keys within the upload_to_s3 function to enable the S3 uploads.

Conclusion
The Redfin Data project automates the ETL process for Redfin market data, making it easy to collect and analyze real estate data. By utilizing Apache Airflow and AWS S3, this project ensures a reliable and efficient data pipeline for your real estate analytics needs.
