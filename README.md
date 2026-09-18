#  Zomato Data Engineering & AI Analytics Platform

An end-to-end **Data Engineering + AI Analytics** platform built around Zomato datasets.

This project demonstrates a modern cloud data pipeline from **Amazon S3 → Snowflake → dbt → Apache Airflow**, enhanced with **Groq LLMs, BGE-M3 embeddings, RAG, Text-to-SQL, and Streamlit**.

---

##  Project Overview

```text
                    ZOMATO DATASETS
                          |
                          v
                  +---------------+
                  |   Amazon S3   |
                  |  Raw Storage  |
                  +-------+-------+
                          |
                          v
                  +---------------+
                  |   Snowflake   |
                  |   RAW Layer   |
                  +-------+-------+
                          |
                          v
                  +---------------+
                  |      dbt      |
                  | STAGING/MARTS |
                  +-------+-------+
                          |
             +------------+------------+
             |                         |
             v                         v
      +-------------+          +-------------+
      | AI Enrichment|          |    RAG      |
      |    Groq      |          |  BGE-M3    |
      +------+------+          +------+------+
             |                         |
             +------------+------------+
                          |
                          v
                  +---------------+
                  | Text-to-SQL   |
                  | Natural Lang. |
                  +-------+-------+
                          |
                          v
                  +---------------+
                  |   Streamlit   |
                  | AI Analytics  |
                  +---------------+

                 Apache Airflow
              orchestrates the flow
```

---

##  Objectives

- Store raw Zomato datasets in Amazon S3.
- Load raw data into Snowflake.
- Transform data using dbt.
- Build staging and analytical mart models.
- Apply dbt data-quality tests.
- Orchestrate the pipeline with Apache Airflow.
- Run Airflow in Docker.
- Enrich customer reviews using Groq.
- Build a review-based RAG application.
- Generate analytical SQL from natural-language questions.
- Execute analytical queries safely against Snowflake.
- Provide interactive AI analytics using Streamlit.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Data processing and AI applications |
| ☁️ Amazon S3 | Raw data storage |
| ❄️ Snowflake | Cloud data warehouse |
| 🔄 dbt | Data transformation and testing |
| ⚙️ Apache Airflow | Pipeline orchestration |
| 🐳 Docker | Containerized Airflow environment |
| 🐘 PostgreSQL | Airflow metadata database |
| 🤖 Groq | LLM inference |
| 🧠 BGE-M3 | Review embeddings |
| 🔎 RAG | Semantic review retrieval |
| 💬 Text-to-SQL | Natural-language data analytics |
| 🎨 Streamlit | Interactive AI applications |
| 🗃️ SQL | Data loading and analytics |
| 🔧 Git/GitHub | Version control |

---

#  Dataset

The project uses:

- Restaurants
- Users
- Food
- Menu
- Orders
- Order Items
- Reviews

Raw CSV datasets are kept locally and/or in Amazon S3 and are intentionally excluded from Git tracking.

---

#  Amazon S3 Layer

S3 acts as the raw cloud-storage layer.

```text
s3://<bucket>/
├── restaurants/
├── users/
├── food/
├── menu/
├── orders/
├── order_items/
└── reviews/
```

Snowflake accesses these files through an **external stage** and a secure **storage integration**.

---

#  Snowflake Data Warehouse

The project uses the:

```text
ZOMATO
```

database.

Main schemas:

```text
ZOMATO
├── RAW
├── STAGING
├── MARTS
└── AI
```

## RAW Tables

```text
ZOMATO.RAW.RESTAURANTS
ZOMATO.RAW.USERS
ZOMATO.RAW.FOOD
ZOMATO.RAW.MENU
ZOMATO.RAW.ORDERS
ZOMATO.RAW.ORDER_ITEMS
ZOMATO.RAW.REVIEWS
```

The RAW layer stores source-oriented data before transformation.

---

#  S3 → Snowflake

```text
Amazon S3
    |
    v
Snowflake Storage Integration
    |
    v
External Stage
    |
    v
COPY INTO
    |
    v
Snowflake RAW Tables
```

The Airflow `reload_raw` task performs the Snowflake `COPY INTO` operations.

---

#  dbt Transformation Layer

The dbt project is located in:

```text
zomato/
```

Architecture:

```text
RAW
 |
 v
STAGING
 |
 v
MARTS
```

## Staging Models

```text
stg_food
stg_menu
stg_order_items
stg_orders
stg_restaurants
stg_reviews
stg_users
```

Staging models are primarily materialized as views.

## Mart Models

### Dimensions

```text
dim_customer
dim_date
dim_food
dim_restaurants
```

### Facts

```text
fct_orders
fact_order_items
```

### Analytical Marts

```text
mart_daily_city_revenune
mart_delivery_sla
mart_restaurant_performance
```

These models support revenue, restaurant, delivery, customer, order, and cancellation analysis.

---

# 🧪 Data Quality

dbt tests are used for:

- `unique`
- `not_null`
- `relationships`
- `accepted_values`
- Source/model validation

The core dbt pipeline was successfully built and tested during development.

---

#  Apache Airflow

The Airflow DAG is:

```text
zomato_batch
```

Main workflow:

```text
reload_raw
     |
     v
dbt_build_core
     |
     v
enrich_reviews
     |
     v
dbt_build_ai
```

### `reload_raw`

Loads raw datasets from the Snowflake external stage into RAW tables.

### `dbt_build_core`

Builds the core dbt models and runs associated tests.

### `enrich_reviews`

Uses Groq to classify and enrich customer reviews.

### `dbt_build_ai`

Builds AI-related dbt models tagged for the AI layer.

---

#  Docker

The Airflow environment is containerized using Docker.

```text
airflow/
├── Dockerfile
├── docker-compose.yaml
└── dags/
    └── zomato_batch.py
```

The Docker image includes:

- Apache Airflow
- Snowflake provider
- FAB authentication
- Groq Python SDK
- dbt-snowflake in a dedicated virtual environment

---

#  AI Review Enrichment

The review enrichment application uses Groq with:

```text
openai/gpt-oss-120b
```

Flow:

```text
Review
  |
  v
Groq LLM
  |
  +--> Sentiment Label
  +--> Sentiment Score
  +--> Topic
  +--> Key Issue
  |
  v
ZOMATO.AI.REVIEW_ENRICHED
```

Supported topics include:

- Food quality
- Delivery
- Pricing
- Service
- Packaging
- Other

Implementation:

```text
ai/enrich_reviews.py
```

---

# 🔎 Retrieval-Augmented Generation (RAG)

The project includes a review-based RAG application.

```text
Zomato Reviews
      |
      v
BGE-M3 Embeddings
      |
      v
Vector Representations
      |
      v
Cosine Similarity Search
      |
      v
Top Relevant Reviews
      |
      v
Groq LLM
      |
      v
Natural Language Answer
```

Implementation:

```text
ai/rag_chat.py
```

The application retrieves relevant customer reviews and supplies them as context to the LLM.

---

#  Text-to-SQL

The project includes natural-language analytics.

Example:

```text
Top 10 cities by GMV
```

Workflow:

```text
Natural Language Question
          |
          v
       Groq LLM
          |
          v
    Generated SQL
          |
          v
     Safety Check
          |
          v
      Snowflake
          |
          v
      DataFrame
          |
          v
    Streamlit Result
```

Implementation:

```text
ai/text_to_sql.py
```

The LLM receives the available analytical schema and generates a SQL query.

---

#  SQL Safety

The Text-to-SQL application includes an application-level safety check.

Queries must begin with:

```text
SELECT
```

or:

```text
WITH
```

It also checks for operations such as:

```text
DROP
DELETE
TRUNCATE
ALTER
UPDATE
INSERT
CREATE
REPLACE
GRANT
REVOKE
```

> This is an application-level safeguard, not a complete security boundary. Database permissions should also restrict the execution role.

---

#  Streamlit Applications

Current AI applications include:

```text
ai/rag_chat.py
ai/text_to_sql.py
```

### RAG

Example:

```text
What are the most common complaints about delivery?
```

### Text-to-SQL

Example:

```text
Top 10 restaurants by revenue
```

---

#  Project Structure

```text
zomato-data-engineering-platform/
│
├── README.md
├── .gitignore
│
├── ai/
│   ├── enrich_reviews.py
│   ├── rag_chat.py
│   └── text_to_sql.py
│
├── airflow/
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   └── dags/
│       └── zomato_batch.py
│
├── review_embeddings.parquet
│
└── zomato/
    ├── dbt_project.yml
    ├── README.md
    ├── analyses/
    ├── macros/
    │   └── generate_schema_name.sql
    ├── models/
    │   ├── staging/
    │   └── marts/
    ├── seeds/
    ├── snapshots/
    └── tests/
```

---

# 🔑 Environment Variables

Store credentials locally in `.env`.

Example:

```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

GROQ_API_KEY=your_groq_api_key
SAMPLE_N=5
```

Never commit real credentials or API keys.

---

# 🚀 Running the Project

## 1. Clone

```bash
git clone https://github.com/charanreddy0006/zomato-data-engineering-platform.git
cd zomato-data-engineering-platform
```

## 2. Configure credentials

Create the required local `.env` configuration.

## 3. Start Airflow

```bash
cd airflow
docker-compose build
docker-compose up -d
```

## 4. Open Airflow

```text
http://localhost:8080
```

## 5. Trigger the DAG

Trigger:

```text
zomato_batch
```

Pipeline:

```text
reload_raw
     ↓
dbt_build_core
     ↓
enrich_reviews
     ↓
dbt_build_ai
```

---


---

#  Future Improvements

- Store embeddings in a persistent vector database.
- Add incremental AI enrichment for larger datasets.
- Replace simple SQL keyword checks with stronger SQL parsing/validation.
- Add automated data-quality monitoring.
- Add Airflow failure notifications.
- Add CI/CD for dbt and Python.
- Deploy Streamlit to the cloud.
- Improve configuration so the project is portable across machines.
- Add automated documentation and testing.

---

#  Security

Never commit:

```text
.env
API keys
Snowflake passwords
AWS credentials
Private keys
profiles.yml
Large raw datasets
```

The repository `.gitignore` excludes sensitive and generated files.

For production environments, use a proper secrets-management solution.

---

#  Repository

GitHub:

https://github.com/charanreddy0006/zomato-data-engineering-platform

---



## ⭐ Project Summary

This project combines modern **Data Engineering and AI Engineering** into one end-to-end platform:

```text
Amazon S3
    ↓
Snowflake
    ↓
dbt
    ↓
Apache Airflow
    ↓
Groq AI
    ↓
BGE-M3
    ↓
RAG
    ↓
Text-to-SQL
    ↓
Streamlit
```

A practical portfolio project demonstrating how cloud data pipelines, analytical data modeling, orchestration, and AI-powered applications can work together.
