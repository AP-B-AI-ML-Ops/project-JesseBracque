"""Monitoring and Reporting for Gold Price Prediction Model"""

from datetime import datetime

import mlflow
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
from mlflow.tracking import MlflowClient
from prefect import flow, task
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import create_database, database_exists

# Set up MLflow
mlflow.set_tracking_uri("http://experiment-tracking:5000")
client = MlflowClient("http://experiment-tracking:5000")
MODEL_NAME = "gold-values-model-mlops-project"

# Database configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "mlflow_db"
DB_URI = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@backend-database:5432/{POSTGRES_DB}"
)

if not database_exists(DB_URI):
    create_database(DB_URI)
ENGINE = create_engine(DB_URI)


@flow(log_prints=True)
def generate_report():
    """Generate a report for the model"""
    year = 2021
    month = 4

    reference_data = pd.read_sql(
        f"SELECT * FROM mlflow_db WHERE year = {year} AND month = {1}", ENGINE
    )
    current_data = pd.read_sql(
        f"SELECT * FROM mlflow_db WHERE year = {year} AND month = {month}", ENGINE
    )

    report = Report(metrics=[DataDriftPreset()])
    snapshot = report.run(reference_data=reference_data, current_data=current_data)

    return snapshot


@flow(log_prints=True)
def extract_data_from_report():
    """Extract data from the report"""
    snapshot = generate_report()
    json_data = snapshot.dict()
    result_data = []
    report_time = datetime.now()

    for metric in json_data["metrics"]:
        metric_id = metric["metric_id"]
        value = metric["value"]

        result_data.append(
            {"run_time": report_time, "metric_name": metric_id, "value": value}
        )

    return result_data


@flow(log_prints=True)
def run_monitoring():
    """Save the report data to the database"""
    result_data = extract_data_from_report()
    metrics_df = pd.DataFrame(result_data)
    metrics_df.to_sql(
        "evidently_metrics",
        ENGINE,
        if_exists="replace",
        index=False,
        dtype={"value": JSON},
    )

if __name__ == "__main__":
    run_monitoring.serve(
        name="save-report-to-db"
    )