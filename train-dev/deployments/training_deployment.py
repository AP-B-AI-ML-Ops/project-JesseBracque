import inspect


import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import prefect
from prefect import flow

from scripts.preprocess_data import run_data_prep
from scripts.train import run_train
from scripts.hpo import run_optimization

@flow(name="full-training-pipeline")
def training_pipeline(
    raw_data_path: str = "./data-files",
    dest_path: str = "./output",
    dataset: str = "Daily.csv",
    num_trials: int = 5
):
    """Runs the complete training pipeline including preprocessing, training and HPO"""
    # Initialize MLflow lazily at runtime
    #def initialize_mlflow():
    #    import mlflow
    #    mlflow.set_tracking_uri("http://localhost:5000")
        # .mlflow.set_experiment("random-forest-hyperopt-MLOps-project-gold-values")
    
    # Step 1: Preprocess data
    run_data_prep(
        raw_data_path=raw_data_path,
        dest_path=dest_path,
        dataset=dataset
    )

    # Step 2: Train basic model
    #initialize_mlflow()
    run_train(data_path=dest_path)

    # Step 3: Run hyperparameter optimization
    run_optimization(
        data_path=dest_path,
        num_trials=num_trials
    )

if __name__ == "__main__":
    training_pipeline.serve(
        name="complete-training-pipeline",
        parameters={
            "raw_data_path": "./data-files",
            "dest_path": "./output",
            "dataset": "Daily.csv",
            "num_trials": 5
        },
        cron="0 0 * * *",  # Daily at midnight
    )