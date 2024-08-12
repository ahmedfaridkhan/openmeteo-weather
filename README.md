# openmeteo-weather

## Project Report: Weather Data Pipeline using Apache Airflow and Docker
https://github.com/ahmedfaridkhan/openmeteo-weather
### 1. Introduction
The project is designed to implement a robust ETL (Extract, Transform, Load) pipeline for weather data ingestion, processing, and storage using Apache Airflow. The pipeline operates within a Docker container, ensuring portability and consistency across different environments. The ETL process is designed to be automated and runs on a daily schedule, ensuring that weather data is up-to-date and readily available for analysis. The final step in the process is the visualization of this data using Tableau, where the data is presented in an interactive dashboard.
### 2. Project Structure and Components
The project is structured around a series of Python scripts and DAGs (Directed Acyclic Graphs) that manage different stages of the ETL process. Below is a breakdown of the key components:
#### 1.	config.py:
o	This script holds configuration settings that are used across various DAGs and tasks. It centralizes the definitions of critical parameters such as API endpoints, database connection strings, and other constants, ensuring ease of maintenance.
#### 2.	model.py:
o	The model.py script defines the schema of the database tables where the weather data is stored. It includes the structure of the tables, specifying the fields for various weather metrics and their data types. This ensures that the data is stored consistently and is easily queryable.
#### 3.	weather_data_migration.py:
o	This script is designed to create the necessary tables in the PostgreSQL database. It defines the schema according to the structure outlined in model.py and ensures that the database is ready to receive data. This script is run only once or when there are changes to the database schema.
#### 4.	weather_data_migration_dag.py:
o	This DAG is responsible for creating the necessary tables in PostgreSQL. It runs whenever there is a need to set up or reset the database schema. It is the first step before populating the database with weather data through weather_dag.py.
#### 5.	weather_data_ingestion.py:
o	This script handles the initial extraction of weather data from the API. It includes functions for making API requests, handling potential errors, and temporarily storing the raw data. It is designed to be resilient against API downtime or rate limits, incorporating retry mechanisms as necessary.
#### 6.	weather_to_db.py:
o	This script is responsible for ingesting weather data from an external API and loading it into a PostgreSQL database. It manages the connection to the API, retrieves data in a structured format, processes it, and ensures that the data is cleaned and validated before storage in the database.
#### 7.	weather_dag.py:
o	This DAG is the core of the weather data pipeline, orchestrating the entire process. It schedules the periodic tasks of data ingestion, processing, and loading into the database. The DAG ensures that tasks are executed in the correct order and manages retries and failure notifications. It runs daily at 12 AM to keep the data updated.
#### 8.	delete_openmeteo_dag.py:
o	This DAG is used to delete the weather data table from the database. This might be necessary when schema changes are required (e.g., adding a new field). Before running weather_data_migration_dag.py to recreate the table, this DAG ensures that the existing table is removed, preventing conflicts.
#### 9.	delete_table.py:
o	Similar to delete_openmeteo_dag.py, this script focuses on deleting specific tables within the database. It is part of the cleanup operations or when deprecating old data models, ensuring that data is removed in a controlled manner.
### 3. Docker Integration
The entire ETL pipeline is deployed within a Docker container, which simplifies the deployment process and ensures consistency across different environments. Docker allows the pipeline to be easily replicated, whether in development, staging, or production environments. The use of Docker also encapsulates all dependencies, making the pipeline highly portable and reducing the risk of environment-related issues.
### 4. Data Visualization with Tableau
The weather data ingested and processed by the pipeline is subsequently visualized using Tableau. An interactive dashboard was created to display the weather forecast for 100 US cities over the next 7 days. The dashboard includes various visualizations such as:
1.	Map Visualization: Displays the geographical distribution of the cities along with their forecast.
2.	Feels Like vs. Actual Temperature: A comparison of the perceived and actual temperatures throughout the day.
3.	Rain and Snowfall: Displays expected precipitation over the forecast period.
4.	Min Max Temperatures: Shows the expected minimum and maximum temperatures for the next 7 days.
5.	Wind Speed by Time of Day: Highlights wind speed variations throughout the day.
The Tableau dashboard is automatically updated daily, in sync with the ETL pipeline. The data is pulled into Tableau directly from the PostgreSQL database.
You can view the interactive Tableau dashboard here.
### 5. Conclusion
This project successfully demonstrates the implementation of a weather data pipeline using Apache Airflow, Docker, and PostgreSQL. The integration of Docker ensures that the entire pipeline is portable and consistent across environments. The processed data is visualized using Tableau, providing insightful visualizations that can be used for further analysis. The project is designed to be scalable, with each component playing a crucial role in ensuring the reliability and accuracy of the weather data.
### 6. Future Works
While the current implementation of the weather data pipeline is comprehensive and functional, there are several areas for future enhancement:
1.	Scaling the Pipeline: Expanding the pipeline to ingest data from multiple weather APIs to enhance data accuracy and provide redundancy in case one API fails.
2.	Real-Time Data Ingestion: Implementing a real-time data ingestion feature that updates the database more frequently (e.g., every hour or every 15 minutes) instead of the current daily schedule.
3.	Advanced Data Analytics: Integrating advanced analytics or machine learning models to predict weather patterns based on historical data stored in the database.
4.	Automated Alerts and Notifications: Adding functionality for automated alerts and notifications based on specific weather conditions (e.g., extreme temperatures, high wind speeds) that could be beneficial for certain user groups.
5.	Deployment on Cloud Platforms: Deploying the entire pipeline on cloud platforms like AWS, GCP, or Azure to enhance scalability, availability, and performance.
6.	User Authentication and Customization: Enhancing the Tableau dashboard by adding user authentication and allowing users to customize their views, such as selecting specific cities or weather parameters of interest.
### 7. References
https://medium.com/jakartasmartcity/data-pipeline-using-apache-airflow-to-import-data-from-public-api-7ff719118ac8
![image](https://github.com/user-attachments/assets/5818c410-f651-4014-9779-ba643c7f57b0)
