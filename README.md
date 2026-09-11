# Zomato Data Engineering Platform

An end-to-end data engineering project for building a Zomato analytics platform using AWS S3, Snowflake, Apache Airflow, dbt, Python, Docker, and SQL.

The project demonstrates a modern cloud-based data pipeline in which raw Zomato datasets are stored in Amazon S3, loaded into Snowflake, transformed using dbt, tested for data quality, and orchestrated using Apache Airflow.

## 1. Project Overview

The main objective of this project is to build a complete data engineering workflow from raw datasets to analytics-ready data.

The pipeline follows this overall flow:

Zomato CSV Datasets
        |
        v
Amazon S3
        |
        v
Snowflake RAW Layer
        |
        v
dbt STAGING Layer
        |
        v
dbt MARTS Layer
        |
        v
Analytics / BI

Apache Airflow is used to orchestrate the pipeline and automate the execution of the Snowflake loading and dbt transformation tasks.

The project is also designed to be extended with AI-powered analytics such as review enrichment, RAG, Text-to-SQL, and a Streamlit dashboard.

---

## 2. Technologies Used

### Python
Used for data processing, automation, and future AI-related components.

### Amazon S3
Used as cloud object storage for the raw Zomato datasets.

### Snowflake
Used as the cloud data warehouse where raw, staging, and analytical data are stored.

### dbt
Used for SQL-based data transformation, data modeling, and data quality testing.

### Apache Airflow
Used to orchestrate and schedule the data pipeline.

### Docker
Used to containerize the Airflow development environment.

### PostgreSQL
Used by Airflow as its metadata database.

### SQL
Used for Snowflake data loading, transformations, modeling, and analytical queries.

### Git and GitHub
Used for source control and project version management.

---

## 3. Dataset

The project works with multiple Zomato datasets.

The datasets include:

- Restaurants
- Users
- Food
- Menu
- Orders
- Order Items
- Reviews

The raw CSV files are kept locally and are intentionally excluded from the GitHub repository because they are large and are not required for storing the source code.

The data is intended to flow through the cloud pipeline:

Local Dataset -> Amazon S3 -> Snowflake

---

## 4. AWS S3 Layer

Amazon S3 acts as the cloud storage layer for the raw datasets.

The datasets are organized into folders such as:

s3://<bucket>/
    restaurants/
    users/
    food/
    menu/
    orders/
    order_items/
    reviews/

This provides a centralized location from which Snowflake can read the raw files.

---

## 5. Snowflake Data Warehouse

Snowflake is used as the main data warehouse.

The project uses a database named:

ZOMATO

The RAW schema contains the source tables loaded from Amazon S3.

The main RAW tables are:

ZOMATO.RAW.restaurants
ZOMATO.RAW.users
ZOMATO.RAW.food
ZOMATO.RAW.menu
ZOMATO.RAW.orders
ZOMATO.RAW.order_items
ZOMATO.RAW.reviews

### S3 to Snowflake Integration

A Snowflake storage integration is configured to securely connect Snowflake with Amazon S3.

An external stage is used to access the files stored in S3.

The pipeline then uses Snowflake COPY INTO commands to load the raw data into the RAW tables.

Example flow:

Amazon S3
    |
    v
Snowflake External Stage
    |
    v
Snowflake RAW Tables

---

## 6. RAW Layer

The RAW layer stores the data in a form close to the original source.

Its main purpose is to provide a reliable landing layer before transformation.

The RAW layer contains source-oriented tables for:

- Restaurants
- Users
- Food
- Menu
- Orders
- Order Items
- Reviews

The RAW layer is not intended to be the final analytical layer.

Instead, it acts as the source for dbt staging models.

---

## 7. dbt Transformation Layer

dbt is used to transform the RAW data into clean and analytics-ready models.

The dbt project is located inside:

zomato/

The project contains:

- Staging models
- Mart models
- Tests
- Macros
- Seeds
- Snapshots
- dbt project configuration

The transformation architecture is:

RAW
  |
  v
STAGING
  |
  v
MARTS

---

## 8. STAGING Layer

The staging layer cleans and standardizes the raw Snowflake tables.

The staging models currently include:

- stg_food
- stg_menu
- stg_order_items
- stg_orders
- stg_restaurants
- stg_reviews
- stg_users

The staging layer provides a clean and consistent foundation for downstream analytical models.

The staging models are configured as views.

Example:

RAW.orders
    |
    v
stg_orders

RAW.reviews
    |
    v
stg_reviews

---

## 9. MARTS Layer

The marts layer contains analytics-ready models designed for business analysis and reporting.

The project contains dimension models, fact models, and analytical marts.

### Dimension Models

- dim_customer
- dim_date
- dim_food
- dim_restaurants

These models provide descriptive information about important business entities.

### Fact Models

- fct_orders
- fact_order_items

These models contain transactional data used for analytical calculations.

### Analytical Models

- mart_daily_city_revenune
- mart_delivery_sla
- mart_restaurant_performance

These models provide higher-level business insights related to revenue, delivery performance, and restaurant performance.

The marts layer is configured primarily with table materializations.

---

## 10. dbt Data Quality Testing

dbt tests are included to validate the transformed data.

The project uses tests to check important data quality rules and relationships between models.

The dbt pipeline can execute:

- Model builds
- Data tests
- Relationship checks
- Source checks

A successful core dbt build has been completed for the current project stage.

The current successful build completed the core models and tests without errors.

---

## 11. Apache Airflow

Apache Airflow is used to orchestrate the data pipeline.

The Airflow environment is containerized using Docker.

The project contains an Airflow DAG:

zomato_batch

The current core pipeline is:

reload_raw
     |
     v
dbt_build_core

### reload_raw

The `reload_raw` task executes Snowflake commands that load data from the external S3 stage into the RAW tables.

The task loads the following datasets:

- restaurants
- users
- food
- menu
- orders
- order_items
- reviews

### dbt_build_core

The `dbt_build_core` task executes the dbt build command.

It builds the core dbt models and runs the associated data quality tests.

The successful execution of these tasks demonstrates the connection between Airflow, Snowflake, and dbt.

---

## 12. Docker Environment

Docker is used to run the Airflow environment consistently.

The project contains:

airflow/
    Dockerfile
    docker-compose.yaml
    dags/
        zomato_batch.py

The Docker-based environment includes the services required to run Airflow and its metadata database.

This makes the project easier to reproduce on another development machine.

---

## 13. Project Structure

The repository is organized as follows:

Zomato_DataPipeline/
|
|-- README.md
|-- .gitignore
|
|-- airflow/
|   |-- Dockerfile
|   |-- docker-compose.yaml
|   |-- dags/
|       |-- zomato_batch.py
|
|-- data/
|   |-- food.csv
|   |-- menu.csv
|   |-- order_items.csv
|   |-- orders.csv
|   |-- restaurant.csv
|   |-- reviews.csv
|   |-- users.csv
|
|-- zomato/
    |-- dbt_project.yml
    |-- README.md
    |-- .gitignore
    |-- models/
    |   |-- staging/
    |   |-- marts/
    |-- macros/
    |-- analyses/
    |-- tests/
    |-- seeds/
    |-- snapshots/

The `data/` directory exists locally but is excluded from Git tracking.

---

## 14. Security

Sensitive credentials are not stored in the GitHub repository.

The project excludes files such as:

- `.env`
- `profiles.yml`
- Credentials
- Private keys
- Generated logs
- dbt target files
- Python virtual environments

Snowflake and AWS credentials should be configured locally when running the project.

Never commit passwords, API keys, access keys, or other secrets to GitHub.

---

## 15. Current Project Status

Completed:

- [x] Prepare Zomato datasets
- [x] Configure Amazon S3
- [x] Upload raw datasets to S3
- [x] Configure Snowflake
- [x] Create Snowflake RAW tables
- [x] Configure S3 to Snowflake integration
- [x] Create Snowflake external stage
- [x] Configure Apache Airflow
- [x] Run Airflow using Docker
- [x] Create Zomato Airflow DAG
- [x] Load RAW data using Airflow
- [x] Configure dbt
- [x] Connect dbt to Snowflake
- [x] Create staging models
- [x] Create mart models
- [x] Configure dbt tests
- [x] Successfully execute the core dbt build

Planned / Future Work:

- [ ] AI-powered review enrichment
- [ ] Review summarization
- [ ] Structured review insights
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] Vector embeddings and vector search
- [ ] Text-to-SQL
- [ ] SELECT-only SQL safety layer
- [ ] Streamlit analytics dashboard
- [ ] Complete AI workflow orchestration with Airflow

---

## 16. Planned AI Architecture

The next stage of the project is intended to add an AI layer on top of the data platform.

The planned architecture is:

                dbt STAGING
                     |
                     v
              Review Data
                     |
                     v
              LLM Enrichment
                     |
                     v
             Enriched Reviews
                     |
          +----------+----------+
          |                     |
          v                     v
        RAG                 Analytics
          |                     |
          v                     v
     Vector Store          Text-to-SQL
          |                     |
          v                     v
      RAG Chat             Snowflake

The AI components will allow users to ask questions about Zomato reviews and
business data using natural language.

---

## 17. Planned RAG Pipeline

The planned Retrieval-Augmented Generation pipeline will use Zomato review data.

Expected flow:

Reviews
   |
   v
Text Processing
   |
   v
Embeddings
   |
   v
Vector Store
   |
   v
Retriever
   |
   v
LLM
   |
   v
Natural Language Answer

The purpose is to allow users to ask questions based on restaurant review information.

---

## 18. Planned Text-to-SQL

A future Text-to-SQL component will allow users to ask analytical questions in natural language.

Example:

"Which city generated the highest revenue?"

The planned flow is:

Natural Language Question
        |
        v
Text-to-SQL Model
        |
        v
Generated SQL
        |
        v
SELECT-only Validation
        |
        v
Snowflake
        |
        v
Result
        |
        v
Natural Language Response

A SELECT-only safety mechanism is planned so that generated queries cannot modify or delete data.

---

## 19. Planned Streamlit Dashboard

A Streamlit application is planned as the presentation layer.

The dashboard will provide an interactive interface for exploring Zomato analytics.

Potential areas include:

- Revenue analysis
- Restaurant performance
- Delivery performance
- Customer analysis
- Food analysis
- Review insights
- Natural-language analytics

---

## 20. How the Components Work Together

The complete platform is designed around the following responsibilities:

AWS S3
- Stores raw source files.

Snowflake
- Stores raw and transformed warehouse data.

dbt
- Transforms raw data.
- Creates staging models.
- Creates analytical marts.
- Runs data quality tests.

Airflow
- Orchestrates the pipeline.
- Controls task dependencies.
- Automates pipeline execution.

Python
- Supports data processing and future AI components.

Docker
- Provides a reproducible Airflow environment.

Streamlit
- Planned user-facing analytics layer.

AI
- Planned enrichment, RAG, and Text-to-SQL layer.

---

## 21. Key Learning Outcomes

This project provides practical experience with:

- Building an end-to-end data pipeline
- Cloud data storage with AWS S3
- Cloud data warehousing with Snowflake
- S3 to Snowflake data ingestion
- External stages and storage integrations
- ELT architecture
- Data transformation using dbt
- Dimensional data modeling
- Fact and dimension tables
- Data quality testing
- Workflow orchestration using Airflow
- Docker-based development
- SQL-based analytics
- Git and GitHub version control
- Designing AI-powered data applications

---

## 22. Repository

GitHub Repository:

https://github.com/charanreddy0006/zomato-data-engineering-platform

The repository contains the source code and configuration required for the project.

Raw datasets and sensitive configuration files are intentionally excluded from the repository.

---

