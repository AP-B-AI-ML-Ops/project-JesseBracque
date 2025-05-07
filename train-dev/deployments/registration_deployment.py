import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prefect import flow
from scripts.register_model import run_register_model

@flow(name="model-registration-pipeline")
def registration_pipeline(
    data_path: str = "./output",
    top_n: int = 10
):
    """Runs the model registration pipeline to register the best model"""
    import mlflow
    mlflow.set_tracking_uri("http://experiment-tracking:5000")

    # Register the best model from HPO runs
    run_register_model(
        data_path=data_path,
        top_n=top_n
    )

if __name__ == "__main__":
    registration_pipeline.serve(
        name="model-registration",
        parameters={
            "data_path": "./output",
            "top_n": 10
        },
        cron="10 0 * * *",  # Daily at 00:10 AM
    )