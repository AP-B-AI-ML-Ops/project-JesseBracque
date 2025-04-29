import os
import pickle
import click

import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

from prefect import task, flow


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)
    

def run_train(data_path: str):
    # set the tracking uri for mlflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # set the experiment for mlflow
    mlflow.set_experiment("gold-values")

    # start an mlflow run
    with mlflow.start_run():
        # set some mlflow tags (e.g. developer)
        mlflow.set_tag("developer", "Jesse") #laatste twee zijn afkortng eigen naam

        # log params in mlflow (e.g. path to the data for validation and training data)
        mlflow.log_param("train-data-path", "./data/green_tripdata_2021-01.parquet")
        mlflow.log_param("valid-data-path", "./data/green_tripdata_2021-02.parquet")

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


if __name__ == '__main__':
    run_train()