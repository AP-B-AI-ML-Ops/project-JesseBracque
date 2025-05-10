"""Training the model for later usage"""

import os
import pickle

import mlflow
from prefect import flow, task
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


@task(log_prints=True, retries=4)
def load_pickle(filename: str):
    """loads pickle file from a file name"""
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@flow(log_prints=True)
def run_train(data_path: str):
    """Training the model and log the output to mlflow"""
    # pylint: disable=[C0103]
    # set the tracking uri for mlflow
    mlflow.set_tracking_uri("http://experiment-tracking:5000") #lets test

    # set the experiment for mlflow
    mlflow.set_experiment("gold-values-experiment-mlops-project")

    # start an mlflow run
    with mlflow.start_run():
        # set some mlflow tags (e.g. developer)
        mlflow.set_tag("developer", "Jesse")  # laatste twee zijn afkortng eigen naam

        # log params in mlflow (e.g. path to the data for validation and training data)
        mlflow.log_param("train-and-val-data-path", "./data-files/daily.csv")

        # Load training and validation data
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        # move the values for the regressor (below) to a variable
        max_depth = 10
        random_state = 0

        # log the values for the regressor in mlflow
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)

        # Train the model
        rf = RandomForestRegressor(max_depth=max_depth, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = root_mean_squared_error(y_val, y_pred)

        # log the rmse in mlflow
        mlflow.log_metric("rmse", rmse)


if __name__ == "__main__":
    run_train("./output")
