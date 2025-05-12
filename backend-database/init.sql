CREATE DATABASE prefect_db;
CREATE DATABASE mlflow_db;


\c mlflow_db;

CREATE TABLE IF NOT EXISTS batch_data (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    Date DATE,
    EUR FLOAT,
    Gold FLOAT
);