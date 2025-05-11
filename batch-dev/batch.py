"""Batch processing script for gold value predictions"""

import os
import pickle
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from prefect import flow, task
# Import the monitoring flow
import sys
sys.path.append('/app')  # Add the app directory to Python path

try:
    from monitoring_reporting.monitor import run_monitoring
except ImportError as e:
    print(f"Warning: Could not import monitoring flow. Make sure the monitoring module is accessible: {e}")
    print("The monitoring directory should be mounted at /app/monitoring_reporting in the Docker container")
    run_monitoring = None

# Set up MLflow
mlflow.set_tracking_uri("http://experiment-tracking:5000")
client = MlflowClient("http://experiment-tracking:5000")
MODEL_NAME = "gold-values-model-mlops-project"

@task(log_prints=True, retries=4)
def prepare_gold_data(df, currency_col="EUR", new_col_name="gold_diff"):
    """Calculates the difference in gold value between two consecutive days"""
    # Convert currency column to numeric, handling any commas in the values
    df[currency_col] = df[currency_col].str.replace(",", "").astype(float)
    df[new_col_name] = df[currency_col].diff()
    df = df.dropna()
    return df

def load_vectorizer():
    """Load the DictVectorizer used during training"""
    try:
        with open("/app/dv.pkl", "rb") as f_in:
            return pickle.load(f_in)
    except Exception as e:
        print(f"Error loading DictVectorizer: {e}")
        raise

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
    # Convert date to string as it was done during training
    df_copy["Date"] = df_copy["Date"].astype(str)
    
    # Create feature dictionaries - same as in training
    categorical = ["Date"]
    numerical = ["EUR"]
    
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
    """Load the latest version of the registered model from MLflow"""
    try:
        # Get the latest version of the registered model
        latest_version = client.get_latest_versions(MODEL_NAME, stages=["None"])[0]
        print(
            f"Loading model version: {latest_version.version} from {latest_version.source}"
        )

        # Load the model using the source URI from the model version
        model = mlflow.pyfunc.load_model(latest_version.source)
        
        # Get the run_id from the run that created this model version
        run_id = latest_version.run_id
        return model, run_id
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

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
    dv = load_vectorizer()
    features_transformed = dv.transform(features)
    predictions = model.predict(features_transformed)
    
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
    
    # Run monitoring after batch predictions
    try:
        print("Running model monitoring...")
        if run_monitoring:
            monitoring_result = run_monitoring()
            if monitoring_result:
                print("Monitoring completed successfully")
            else:
                print("Warning: Monitoring completed but returned no results")
        else:
            print("Warning: Monitoring flow not available")
    except Exception as e:
        print(f"Warning: Error running monitoring: {e}")

    return output_file

if __name__ == "__main__":
    run_batch.serve(
        name="daily-gold-predictions",
        parameters={
            "filename": "app/data-files/Daily.csv",
            "output_path": "/batch-data/predictions"
        }
    )