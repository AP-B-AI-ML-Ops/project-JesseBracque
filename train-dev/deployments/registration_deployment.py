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
        work_pool_name="main",
        parameters={
            "data_path": "./output",
            "top_n": 10
        }
    )