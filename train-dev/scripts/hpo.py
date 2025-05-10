""" "Hyper parameter optimization"""

import os
import pickle

import mlflow
import optuna
from optuna.samplers import TPESampler
from prefect import flow, task
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


# Check if running locally or in container
if os.getenv("DOCKER_CONTAINER", "false") == "true":
    tracking_uri = "http://experiment-tracking:5000"
else:
    tracking_uri = "http://localhost:5000"
    
# set the tracking uri for mlflow
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_experiment("gold-values-experiment-mlops-project")


@task(log_prints=True, retries=4)
def load_pickle(filename):
    """loads pickle file from a file name"""
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@flow(log_prints=True)
def run_optimization(data_path: str, num_trials: int):
    """ "main function, runs the hop training from a given path for a given number of trails"""
    # pylint: disable=[C0103]
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 10, 50, 1),
            "max_depth": trial.suggest_int("max_depth", 1, 20, 1),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 10, 1),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 4, 1),
            "random_state": 42,
            "n_jobs": -1,
        }

        # start an mlflow run
        with mlflow.start_run():

            # log the params to mlflow
            mlflow.log_params(params)

            rf = RandomForestRegressor(**params)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_val)
            rmse = root_mean_squared_error(y_val, y_pred)

            # log the rmse to mlflow
            mlflow.log_metric("rmse", rmse)

        return rmse

    sampler = TPESampler(seed=42)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=num_trials)


if __name__ == "__main__":
    run_optimization("./output", 5)
