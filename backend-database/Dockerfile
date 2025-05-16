FROM postgres:15

COPY ./00_init.sql /docker-entrypoint-initdb.d/00_init.sql
COPY ./01_mlflow_db_schema.sql /docker-entrypoint-initdb.d/01_mlflow_db_schema.sql

