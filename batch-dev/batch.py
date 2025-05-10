"""Batch processing script for gold value predictions"""

import os
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from prefect import flow, task
from sklearn.feature_extraction import DictVectorizer

# Set up MLflow
mlflow.set_tracking_uri("http://experiment-tracking:5000")
client = MlflowClient("http://experiment-tracking:5000")
MODEL_NAME = "gold-values-model-mlops-project"

@task(log_prints=True, retries=4)
def prepare_gold_data(df, currency_col="EUR", new_col_name="gold_diff"):
    """Calculates the difference in gold value between two consecutive days"""
    df[new_col_name] = df[currency_col].diff()
    df = df.dropna()
    return df

@task(log_prints=True, retries=4)
def prepare_features(df):
    """Prepare features for prediction"""
    df_copy = df.copy()
    
    # Convert numeric columns
    for col in df_copy.columns:
        if col != "Date":
            if isinstance(df_copy[col], str):
                df_copy[col] = df_copy[col].str.replace(",", "", regex=False)
            df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
    
    df_copy["Date"] = pd.to_datetime(df_copy["Date"])
    
    # Create feature dictionaries
    categorical = []  # Add categorical columns if any
    numerical = ["EUR", "USD", "GBP", "CHF", "CNY", "JPY"]  # Add all your currency columns
    
    dicts = df_copy[categorical + numerical].to_dict(orient="records")
    return dicts

@task(log_prints=True, retries=4)
def get_latest_version():
    """Get the latest version of the registered model"""
    try:
        # Get the experiment to find the latest run
        experiment = client.get_experiment_by_name("gold-values-experiment-mlops-project")
        if experiment is None:
            raise Exception("Experiment not found")
            
        # Get the latest successful run
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            max_results=1,
            order_by=["metrics.test_rmse ASC"]
        )
        
        if not runs:
            raise Exception("No runs found in the experiment")
            
        run_id = runs[0].info.run_id
        print(f"Loading model from run: {run_id}")
        return run_id
    except Exception as e:
        print(f"Error getting latest version: {e}")
        raise

@flow(log_prints=True)
def load_model():
    """Load the latest model from MLflow"""
    print("Loading model...")
    run_id = get_latest_version()
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.pyfunc.load_model(model_uri)
    return model, run_id

@task(log_prints=True, retries=4)
def read_data(filename: str):
    """Read and prepare the data for prediction"""
    print(f"Reading data from {filename}")
    df = pd.read_csv(filename)
    return df

@flow(log_prints=True)
def run_batch(filename: str, output_path: str):
    """Run batch predictions on the provided data"""
    # Load model and data
    model, run_id = load_model()
    df = read_data(filename)
    
    print("Preparing data for prediction...")
    df_prepared = prepare_gold_data(df)
    features = prepare_features(df_prepared)
    
    print("Making predictions...")
    predictions = model.predict(features)
    
    # Create results DataFrame
    print("Creating results DataFrame...")
    df_result = pd.DataFrame()
    df_result["Date"] = df_prepared["Date"]
    df_result["Actual_EUR"] = df_prepared["EUR"]
    df_result["Predicted_Next_Day_Change"] = predictions
    df_result["model_run_id"] = run_id
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Save results
    output_file = os.path.join(output_path, f"predictions_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv")
    print(f"Saving predictions to: {output_file}")
    df_result.to_csv(output_file, index=False)
    
    return output_file

if __name__ == "__main__":
    run_batch.serve(
        name="daily-gold-predictions",
        parameters={
            "filename": "data-files/Daily.csv",
            "output_path": "/batch-data/predictions"
        }
    )