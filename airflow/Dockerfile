# Airflow 3.x image + Snowflake provider + FAB auth
# + dbt venv + Groq AI
FROM apache/airflow:3.0.3


# ------------------------------------------------------------
# Airflow Providers + Groq
# ------------------------------------------------------------

RUN pip install --no-cache-dir \
      apache-airflow-providers-snowflake \
      apache-airflow-providers-fab \
      groq


# ------------------------------------------------------------
# dbt in a separate virtual environment
# ------------------------------------------------------------

RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir \
      "dbt-snowflake==1.8.*"