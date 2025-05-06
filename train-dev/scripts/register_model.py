"""Registering the model for later usage"""

import os
import pickle

import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from prefect import flow, task
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

HPO_EXPERIMENT_NAME = "random-forest-hyperopt-MLOps-project-gold-values"
EXPERIMENT_NAME = "random-forest-best-models-MLOps-project-gold-values"
MODEL_NAME = "random-forest-regressor-MLOps-project-gold-values"

RF_PARAMS = [
    "max_depth",
    "n_estimators",
    "min_samples_split",
    "min_samples_leaf",
    "random_state",
    "n_jobs",
]

mlflow.set_tracking_uri("http://experiment-tracking:5000")
mlflow.set_experiment(EXPERIMENT_NAME)


@task(log_prints=True, retries=4)
def load_pickle(filename):
    """loads pickle file from a file name"""
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@flow(log_prints=True)
def train_and_log_model(data_path, params):
    """Train the model and log the output to mlflow"""
    # pylint: disable=[C0103]
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
    X_test, y_test = load_pickle(os.path.join(data_path, "test.pkl"))

    with mlflow.start_run():
        for param in RF_PARAMS:
            params[param] = int(params[param])

        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)

        # Evaluate model on the validation and test sets
        val_rmse = root_mean_squared_error(y_val, rf.predict(X_val))
        mlflow.log_metric("val_rmse", val_rmse)
        test_rmse = root_mean_squared_error(y_test, rf.predict(X_test))
        mlflow.log_metric("test_rmse", test_rmse)

        # Log the model
        mlflow.sklearn.log_model(rf, artifact_path="model")


@flow(log_prints=True)
def run_register_model(data_path: str, top_n: int):
    """Run the register model flow"""
    client = MlflowClient()

    experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.rmse ASC"],
    )
    for run in runs:
        train_and_log_model(data_path=data_path, params=run.data.params)

    # Select the model with the lowest test RMSE by using the method search_runs()
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.test_rmse ASC"],
    )[0]

    # Register the best model by using the method register_model()
    # get the run id
    best_run_id = best_run.info.run_id

    # get the model uri (using the run id)
    model_uri = f"runs:/{best_run_id}/model"

    # register the model
    mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)


if __name__ == "__main__":
    run_register_model("./output", 10)
