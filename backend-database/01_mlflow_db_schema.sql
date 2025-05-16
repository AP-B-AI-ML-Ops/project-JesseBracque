CREATE DATABASE batch_db;

\connect batch_db

CREATE TABLE IF NOT EXISTS batch_data (
    id SERIAL PRIMARY KEY,
    date DATE,
    eur FLOAT NOT NULL,
    gold_diff FLOAT NOT NULL
);