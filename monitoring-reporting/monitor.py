import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import psycopg
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import mlflow
from prefect import flow, task
from prefect.logging import get_run_logger

# Database configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "mlflow_db"

@task(retries=3, retry_delay_seconds=60)
def get_db_connection():
    """Create database connection"""
    logger = get_run_logger()
    connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(connection_string)
    
    if not database_exists(engine.url):
        logger.info("Database does not exist. Creating...")
        create_database(engine.url)
    
    return engine

@task
def load_reference_data():
    """Load reference data (training data)"""
    logger = get_run_logger()
    logger.info("Loading reference data...")
    train_data = pd.read_csv('data-files/gold_train.csv')
    logger.info(f"Loaded reference data with shape {train_data.shape}")
    return train_data

@task
def load_current_data():
    """Load current data from the predictions database"""
    logger = get_run_logger()
    engine = get_db_connection()
    query = """
    SELECT * FROM gold_predictions 
    WHERE prediction_time >= NOW() - INTERVAL '1 day'
    """
    current_data = pd.read_sql(query, engine)
    logger.info(f"Loaded current data with shape {current_data.shape}")
    return current_data

@task
def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare data for monitoring"""
    logger = get_run_logger()
    logger.info("Preparing data...")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@task(retries=2)
def calculate_metrics(reference_data: pd.DataFrame, current_data: pd.DataFrame):
    """Calculate drift metrics using Evidently"""
    logger = get_run_logger()
    logger.info("Calculating drift metrics...")
    
    column_mapping = ColumnMapping(
        target="Gold",
        numerical_features=['EUR'],
        categorical_features=['Date'],
        prediction='prediction'
    )
    
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    
    return data_drift_report

@task
def save_metrics(report, engine):
    """Save metrics to the database"""
    logger = get_run_logger()
    metrics_dict = report.as_dict()
    
    # Extract relevant metrics
    drift_score = metrics_dict['metrics'][0]['result']['dataset_drift']['drift_score']
    num_drifted_features = metrics_dict['metrics'][0]['result']['dataset_drift']['number_of_drifted_features']
    
    logger.info(f"Drift score: {drift_score}")
    logger.info(f"Number of drifted features: {num_drifted_features}")
    
    # Create metrics table if not exists
    with engine.connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_metrics (
            timestamp TIMESTAMP,
            drift_score FLOAT,
            num_drifted_features INTEGER
        )
        """)
        
        # Insert metrics
        conn.execute("""
        INSERT INTO monitoring_metrics (timestamp, drift_score, num_drifted_features)
        VALUES (%s, %s, %s)
        """, (datetime.now(), drift_score, num_drifted_features))
        conn.commit()
    
    logger.info("Metrics saved to database")

@flow(name="gold-model-monitoring", log_prints=True)
def run_monitoring():
    """Main monitoring flow"""
    logger = get_run_logger()
    
    # Get database connection
    engine = get_db_connection()
    
    # Load data
    reference_data = load_reference_data()
    current_data = load_current_data()
    
    if current_data.empty:
        logger.warning("No predictions found in the last day. Skipping monitoring.")
        return
    
    # Prepare data
    reference_data = prepare_data(reference_data)
    current_data = prepare_data(current_data)
    
    # Calculate metrics
    report = calculate_metrics(reference_data, current_data)
    
    # Save metrics
    save_metrics(report, engine)
    
    logger.info("Monitoring complete. Metrics saved to database.")
    return True

if __name__ == "__main__":
    run_monitoring()
